import { useState, useMemo, useEffect } from "react"
import {
  Modal, TextInput, Stack, Select, Box,
  Paper, Divider, Alert, ThemeIcon, Group, Text, Button,
} from "@mantine/core"
import { useForm } from "@mantine/form"
import { IconAlertCircle, IconShield } from "@tabler/icons-react"
import {
  useUpdateUserMutation,
  useGetRolesQuery,
  useGetDepartmentsQuery,
  useGetMeQuery,
} from "../../services/iamApi"
import type { User, Policy } from "../../types"
import PolicyCard from "./PolicyCard"

const PLATFORM_ROLES = new Set([
  "platform.admin",
  "platform.viewer",
])

const HIDDEN_ROLES = new Set([
  "platform.admin", "platform.viewer", "dept.admin", "dept.viewer",
])

interface Props {
  user: User | null
  onClose: () => void
}

export default function EditUserModal({ user, onClose }: Props) {
  const [error, setError] = useState<string | null>(null)
  const [managementRole, setManagementRole] = useState<string | null>(null)
  const [systemRoles, setSystemRoles] = useState<Record<string, string>>({})

  const { data: me } = useGetMeQuery()
  const { data: roles } = useGetRolesQuery()
  const { data: departments } = useGetDepartmentsQuery()
  const [updateUser, { isLoading }] = useUpdateUserMutation()

  const isSuperuser = me?.is_superuser ?? false
  const isPlatformAdmin = !isSuperuser && (me?.permissions?.includes("iam.user.update_dept") ?? false)
  const isDeptAdmin = !isSuperuser && !isPlatformAdmin

  const form = useForm({
    initialValues: {
      first_name: "",
      last_name: "",
      email: "",
      department: "",
    },
    validate: {
      first_name: (v) => (v.trim() ? null : "First name is required"),
      last_name: (v) => (v.trim() ? null : "Last name is required"),
      email: (v) => (v?.trim() ? null : "Email is required"),
      department: (v) => (isDeptAdmin ? null : v?.trim() ? null : "Department is required"),
    },
  })

  useEffect(() => {
    if (!user) return

    form.setValues({
      first_name: user.first_name ?? "",
      last_name: user.last_name ?? "",
      email: user.email ?? "",
      department: user.department?.id ?? "",
    })

    if (roles) {
      const userRoleCodes = user.roles
      const mgmtRole = userRoleCodes.find((code) => HIDDEN_ROLES.has(code))
      setManagementRole(mgmtRole ?? null)

      const sysRoles: Record<string, string> = {}
      userRoleCodes
        .filter((code) => !HIDDEN_ROLES.has(code))
        .forEach((code) => {
          const role = roles.find((r) => r.code === code)
          if (role) sysRoles[role.system] = role.id
        })
      setSystemRoles(sysRoles)
    }
  }, [user, roles])

  const myDept = useMemo(() => {
    if (!isDeptAdmin || !me?.department || !departments) return null
    return departments.find((d) => d.code === me.department.code) ?? null
  }, [isDeptAdmin, me, departments])

  const selectedDeptId = isDeptAdmin ? (myDept?.id ?? "") : form.values.department
  const selectedDept = departments?.find((d) => d.id === selectedDeptId)
//   const allowedSystems = selectedDept?.allowed_systems ?? []
  const hasDepartment = isDeptAdmin ? !!myDept : !!form.values.department
  const allSystems = [...new Set(roles?.map((r) => r.system).filter((s) => !['iam', 'dept', 'platform'].includes(s)) ?? [])]
  const isPlatformManagementRole = !!managementRole && PLATFORM_ROLES.has(managementRole)
  const allowedSystems = hasDepartment
    ? (isPlatformManagementRole ? allSystems : (selectedDept?.allowed_systems ?? []))
    : []

  const managementRoleOptions = useMemo(() => {
    if (isDeptAdmin) return []
    const isGlobal = selectedDept?.code === "GLOBAL"
    const base = [{ value: "", label: "None" }]
    if (isSuperuser) {
      if (isGlobal) {
        return [...base, { value: "platform.viewer", label: "Platform Viewer" }, { value: "platform.admin", label: "Platform Admin" }]
      }
      return [...base, { value: "dept.viewer", label: "Department Viewer" }, { value: "dept.admin", label: "Department Admin" }, { value: "platform.viewer", label: "Platform Viewer" }, { value: "platform.admin", label: "Platform Admin" }]
    }
    if (isGlobal) return base
    return [...base, { value: "dept.viewer", label: "Department Viewer" }, { value: "dept.admin", label: "Department Admin" }]
  }, [isSuperuser, isDeptAdmin, selectedDept])

  const getRolesForSystem = (system: string) =>
    roles?.filter((r) => r.system === system && !HIDDEN_ROLES.has(r.code)) ?? []

  const resolvedPolicies = useMemo(() => {
    const seen = new Set<string>()
    const result: { policy: Policy; color: string }[] = []

    if (managementRole) {
      roles?.find((r) => r.code === managementRole)?.policies.forEach((p) => {
        if (!seen.has(p.id)) { seen.add(p.id); result.push({ policy: p, color: "blue" }) }
      })
    }

    Object.entries(systemRoles).filter(([, id]) => id).forEach(([, id]) => {
      roles?.find((r) => r.id === id)?.policies.forEach((p) => {
        if (!seen.has(p.id)) { seen.add(p.id); result.push({ policy: p, color: "teal" }) }
      })
    })

    return result
  }, [managementRole, systemRoles, roles])

  const closeModal = () => {
    onClose()
    setError(null)
    form.reset()
    setManagementRole(null)
    setSystemRoles({})
  }

  const handleSubmit = async (values: typeof form.values) => {
    if (!user) return
    setError(null)

    const deptId = isDeptAdmin ? (myDept?.id ?? "") : values.department
    if (!deptId) { setError("Department is required"); return }

    const systemRoleIds = Object.values(systemRoles).filter(Boolean)
    const managementRoleId = managementRole ? roles?.find((r) => r.code === managementRole)?.id : null
    const allRoleIds = [...(managementRoleId ? [managementRoleId] : []), ...systemRoleIds]

    if (allRoleIds.length === 0) { setError("User must have at least one role"); return }

    try {
      await updateUser({
        id: user.id,
        body: { ...values, department: deptId, roles: allRoleIds } as any,
      }).unwrap()
      closeModal()
    } catch (err: any) {
      const data = err?.data
      const fieldError = data?.email?.[0] ?? data?.first_name?.[0] ?? data?.last_name?.[0]
      setError(fieldError ?? data?.detail ?? data?.message ?? "Failed to update user")
    }
  }

  const departmentOptions = departments?.map((d) => ({ value: d.id, label: d.name })) ?? []
  const hasSelectedRoles = managementRole || Object.values(systemRoles).some(Boolean)

  return (
    <Modal
      opened={!!user}
      onClose={closeModal}
      title={
        <Group gap="sm">
          <ThemeIcon variant="light" size="lg"><IconShield size={18} /></ThemeIcon>
          <Box>
            <Text fw={600}>Edit User — {user?.username}</Text>
            <Text size="xs" c="dimmed">Update Access Configuration</Text>
          </Box>
        </Group>
      }
      size="lg"
    >
      {error && <Alert icon={<IconAlertCircle size={16} />} color="red" mb="md">{error}</Alert>}

      <form onSubmit={form.onSubmit(handleSubmit)}>
        <Stack gap="md">

          <TextInput label="Username" value={user?.username ?? ""} disabled />
          <TextInput required label="First Name" {...form.getInputProps("first_name")} />
          <TextInput required label="Last Name" {...form.getInputProps("last_name")} />
          <TextInput required label="Email" {...form.getInputProps("email")} />

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
                form.setFieldValue("department", val ?? "")
                setManagementRole(null)
                setSystemRoles({})
              }}
            />
          )}

          {!isDeptAdmin && (
            <>
              <Divider label="Management Role" labelPosition="left" />
              <Select
                placeholder={hasDepartment ? "--" : "Select a department first"}
                data={managementRoleOptions}
                value={managementRole}
                onChange={(val) => {
                  setManagementRole(val)
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
                }}
                clearable
                disabled={!hasDepartment}
              />
            </>
          )}

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
                        onChange={(val) => setSystemRoles((prev) => ({ ...prev, [system]: val ?? "" }))}
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

          {hasSelectedRoles && (
            <>
              <Divider label="Policies" labelPosition="left" />
              <Stack gap="xs">
                {resolvedPolicies.map(({ policy, color }) => (
                  <PolicyCard key={policy.id} policy={policy} color={color} />
                ))}
                <Text size="xs" c="dimmed" mt={4}>
                  These policies are auto-assigned from selected roles and cannot be changed at update.
                </Text>
              </Stack>
            </>
          )}

          <Divider />

          <Group justify="flex-end">
            <Button variant="default" onClick={closeModal}>Cancel</Button>
            <Button type="submit" loading={isLoading}>Save</Button>
          </Group>
        </Stack>
      </form>
    </Modal>
  )
}
