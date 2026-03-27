import { useState, useMemo } from "react";
import {
  Modal, TextInput, PasswordInput, Stack, Select, Box,
  Paper, Divider, Alert, ThemeIcon, Group, Text, Button,
} from "@mantine/core";
import { useForm } from "@mantine/form";
import { IconAlertCircle, IconShield } from "@tabler/icons-react";
import {
  useCreateUserMutation,
  useGetRolesQuery,
  useGetDepartmentsQuery,
  useGetMeQuery,
} from "../../services/iamApi";
import type { CreateUserPayload, Policy } from "../../types";
import PolicyCard from "./PolicyCard";

const PLATFORM_ROLES = new Set([
  "platform.admin",
  "platform.viewer",
])

const HIDDEN_ROLES = new Set([
  "platform.admin",
  "platform.viewer",
  "dept.admin",
  "dept.viewer",
]);

interface Props {
  opened: boolean;
  onClose: () => void;
}

export default function CreateUserModal({ opened, onClose }: Props) {
  const [error, setError] = useState<string | null>(null);
  const [managementRole, setManagementRole] = useState<string | null>(null);
  const [systemRoles, setSystemRoles] = useState<Record<string, string>>({});

  const { data: me } = useGetMeQuery();
  const { data: roles } = useGetRolesQuery();
  const { data: departments } = useGetDepartmentsQuery();
  const [createUser, { isLoading: isCreating }] = useCreateUserMutation();

  const isSuperuser = me?.is_superuser ?? false;
  const isPlatformAdmin = !isSuperuser && (me?.roles?.includes("platform.admin") ?? false);
  const isDeptAdmin = !isSuperuser && !isPlatformAdmin;

  const form = useForm<Omit<CreateUserPayload, "roles">>({
    initialValues: {
      username: "",
      password: "",
      first_name: "",
      last_name: "",
      email: "",
      department: "",
    },
    validate: {
      username: (v) => (v.trim() ? null : "Username is required"),
      password: (v) => (v.trim() ? null : "Password is required"),
      first_name: (v) => (v.trim() ? null : "First name is required"),
      last_name: (v) => (v.trim() ? null : "Last name is required"),
      email: (v) => (v?.trim() ? null : "Email is required"),
      department: (v) => (isDeptAdmin ? null : v?.trim() ? null : "Department is required"),
    },
  });

  const myDept = useMemo(() => {
    if (!isDeptAdmin || !me?.department || !departments) return null;
    return departments.find((d) => d.code === me.department.code) ?? null;
  }, [isDeptAdmin, me, departments]);

  const selectedDeptId = isDeptAdmin ? (myDept?.id ?? "") : form.values.department;
  const selectedDept = departments?.find((d) => d.id === selectedDeptId);
//   const allowedSystems = selectedDept?.allowed_systems ?? [];
  const hasDepartment = isDeptAdmin ? !!myDept : !!form.values.department;
  const allSystems = [...new Set(roles?.map((r) => r.system).filter((s) => !['iam', 'dept', 'platform'].includes(s)) ?? [])]
  const isPlatformManagementRole = !!managementRole && PLATFORM_ROLES.has(managementRole)
  const allowedSystems = hasDepartment
    ? (isPlatformManagementRole ? allSystems : (selectedDept?.allowed_systems ?? []))
    : []

  const managementRoleOptions = useMemo(() => {
    if (isDeptAdmin) return [];

    const isGlobal = selectedDept?.code === "GLOBAL"
    const base = [{ value: "", label: "None" }]

    if (isSuperuser) {
        if (isGlobal) {
        return [
            ...base,
            { value: "platform.viewer", label: "Platform Viewer" },
            { value: "platform.admin", label: "Platform Admin" },
        ]
        }
        return [
        ...base,
        { value: "dept.viewer", label: "Department Viewer" },
        { value: "dept.admin", label: "Department Admin" },
        { value: "platform.viewer", label: "Platform Viewer" },
        { value: "platform.admin", label: "Platform Admin" },
        ]
    }

    // Platform admin — only dept roles, and only for real departments
    if (isGlobal) return base  // no management role options for GLOBAL
    return [
        ...base,
        { value: "dept.viewer", label: "Department Viewer" },
        { value: "dept.admin", label: "Department Admin" },
    ]
    }, [isSuperuser, isDeptAdmin, selectedDept]);


  const getRolesForSystem = (system: string) =>
    roles?.filter((r) => r.system === system && !HIDDEN_ROLES.has(r.code)) ?? [];

  const closeModal = () => {
    onClose();
    setError(null);
    form.reset();
    setManagementRole(null);
    setSystemRoles({});
  };

  const handleSubmit = async (values: Omit<CreateUserPayload, "roles">) => {
    setError(null);

    const deptId = isDeptAdmin ? (myDept?.id ?? "") : values.department;
    if (!deptId) {
      setError("Department is required");
      return;
    }

    const systemRoleIds = Object.values(systemRoles).filter(Boolean);
    const managementRoleId = managementRole
      ? roles?.find((r) => r.code === managementRole)?.id
      : null;
    const allRoleIds = [
      ...(managementRoleId ? [managementRoleId] : []),
      ...systemRoleIds,
    ];

    if (allRoleIds.length === 0) {
      setError("User must have at least one role");
      return;
    }

    try {
      await createUser({ ...values, department: deptId, roles: allRoleIds }).unwrap();
      closeModal();
    } catch (err: any) {
      const data = err?.data;
      const fieldError =
        data?.username?.[0] ??
        data?.email?.[0] ??
        data?.password?.[0] ??
        data?.first_name?.[0] ??
        data?.last_name?.[0];
      setError(fieldError ?? data?.detail ?? data?.message ?? "Failed to create user");
    }
  };

  const departmentOptions =
    departments?.map((d) => ({ value: d.id, label: d.name })) ?? [];

  const hasSelectedRoles =
    managementRole || Object.values(systemRoles).some(Boolean);

  // Deduplicated policies from all selected roles
  const resolvedPolicies = useMemo(() => {
    const seen = new Set<string>();
    const result: { policy: Policy; color: string }[] = [];

    if (managementRole) {
      const role = roles?.find((r) => r.code === managementRole);
      role?.policies.forEach((p) => {
        if (!seen.has(p.id)) {
          seen.add(p.id);
          result.push({ policy: p, color: "blue" });
        }
      });
    }

    Object.entries(systemRoles)
      .filter(([, id]) => id)
      .forEach(([, id]) => {
        const role = roles?.find((r) => r.id === id);
        role?.policies.forEach((p) => {
          if (!seen.has(p.id)) {
            seen.add(p.id);
            result.push({ policy: p, color: "teal" });
          }
        });
      });

    return result;
  }, [managementRole, systemRoles, roles]);

  return (
    <Modal
      opened={opened}
      onClose={closeModal}
      title={
        <Group gap="sm">
          <ThemeIcon variant="light" size="lg">
            <IconShield size={18} />
          </ThemeIcon>
          <Box>
            <Text fw={600}>IAM Role Assignment</Text>
            <Text size="xs" c="dimmed">Access Control Configuration</Text>
          </Box>
        </Group>
      }
      size="lg"
    >
      {error && (
        <Alert icon={<IconAlertCircle size={16} />} color="red" mb="md">
          {error}
        </Alert>
      )}

      <form onSubmit={form.onSubmit(handleSubmit)}>
        <Stack gap="md">

          {/* Basic Info */}
          <TextInput required label="Username" placeholder="john.doe" {...form.getInputProps("username")} />
          <PasswordInput required label="Password" placeholder="••••••••" {...form.getInputProps("password")} />
          <TextInput required label="First Name" placeholder="John" {...form.getInputProps("first_name")} />
          <TextInput required label="Last Name" placeholder="Doe" {...form.getInputProps("last_name")} />
          <TextInput required label="Email" placeholder="john@example.com" {...form.getInputProps("email")} />

          {/* Department */}
          {isDeptAdmin ? (
            <TextInput label="Department" value={myDept?.name ?? ""} disabled />
          ) : (
            <Select
              required
              label="Department"
              placeholder="Select department"
              data={departmentOptions}
              {...form.getInputProps("department")}
              onChange={(val) => {
                form.setFieldValue("department", val ?? "");
                setManagementRole(null);
                setSystemRoles({});
              }}
            />
          )}

          {/* Management Role */}
          {!isDeptAdmin && (
            <>
              <Divider label="Management Role" labelPosition="left" />
              <Select
                placeholder={hasDepartment ? "--" : "Select a department first"}
                data={managementRoleOptions}
                value={managementRole}
                onChange={(val) => {
                  setManagementRole(val)

                  // Only auto-select system roles for platform-level roles
                  const isPlatformRole = val === "platform.admin" || val === "platform.viewer"

                  if (isPlatformRole && allowedSystems.length > 0) {
                    const suffix = val.endsWith(".admin") ? "admin" : "viewer"
                    const autoSelected: Record<string, string> = {}
                    for (const system of allowedSystems) {
                      const match = roles?.find((r) => r.code === `${system}.${suffix}`)
                      if (match) autoSelected[system] = match.id
                    }
                    setSystemRoles(autoSelected)
                  } else if (!val) {
                    setSystemRoles({})
                  }
                  // dept.admin / dept.viewer → leave system roles as-is
                }}
                clearable
                disabled={!hasDepartment}
              />
            </>
          )}

          {/* System Roles */}
          {allowedSystems.length > 0 && (
            <>
              <Divider label="System Roles" labelPosition="left" />
              <Stack gap="xs">
                {allowedSystems.map((system) => (
                  <Paper key={system} withBorder p="sm">
                    <Group justify="space-between" align="center">
                      <Text size="sm" c="dimmed" ff="monospace" w={100}>{system}</Text>
                      <Select
                        placeholder={hasDepartment ? "Select role" : "Select a department first"}
                        data={getRolesForSystem(system).map((r) => ({ value: r.id, label: r.name }))}
                        value={systemRoles[system] ?? null}
                        onChange={(val) =>
                          setSystemRoles((prev) => ({ ...prev, [system]: val ?? "" }))
                        }
                        clearable
                        disabled={!hasDepartment}
                        style={{ flex: 1 }}
                      />
                    </Group>
                  </Paper>
                ))}
              </Stack>
            </>
          )}

          {/* Policies — deduplicated, read only */}
          {hasSelectedRoles && (
            <>
              <Divider label="Policies" labelPosition="left" />
              <Stack gap="xs">
                {resolvedPolicies.map(({ policy, color }) => (
                  <PolicyCard key={policy.id} policy={policy} color={color} />
                ))}
                <Text size="xs" c="dimmed" mt={4}>
                  These policies are auto-assigned from selected roles and cannot be changed at creation.
                </Text>
              </Stack>
            </>
          )}

          <Divider />

          <Group justify="flex-end">
            <Button variant="default" onClick={closeModal}>Cancel</Button>
            <Button type="submit" loading={isCreating}>Submit</Button>
          </Group>
        </Stack>
      </form>
    </Modal>
  );
}
