import { useState, useMemo, useEffect, useCallback, useRef } from "react"
import {
  Modal, TextInput, Stack, Select, Box,
  Paper, Divider, Alert, ThemeIcon, Group, Text, Button,
  Checkbox, Collapse, UnstyledButton,
} from "@mantine/core"
import { useForm } from "@mantine/form"
import { IconAlertCircle, IconShield, IconChevronDown, IconChevronUp } from "@tabler/icons-react"
import {
  useUpdateUserMutation,
  useGetRoleFormOptionsQuery,
  useGetDepartmentsQuery,
  useGetMeQuery,
  useGetUserQuery,
  useGetPermissionsQuery,
} from "../../services/iamApi"
import type { User, Permission, RoleRef } from "../../types"

interface Props {
  user: User | null
  onClose: () => void
}

export default function EditUserModal({ user, onClose }: Props) {
  const [error, setError] = useState<string | null>(null)
  const [managementRole, setManagementRole] = useState<string | null>(null)
  const [systemRoles, setSystemRoles] = useState<Record<string, string>>({})
  const [selectedPermissionIds, setSelectedPermissionIds] = useState<string[]>([])
  const [showExtraPerms, setShowExtraPerms] = useState(false)
  const initializedRef = useRef(false)

  const { data: me } = useGetMeQuery()
  const { data: departments } = useGetDepartmentsQuery()
  const { data: allPermissions } = useGetPermissionsQuery()
  const { data: userDetail } = useGetUserQuery(user?.id ?? "", { skip: !user, refetchOnMountOrArgChange: true })
  const [updateUser, { isLoading }] = useUpdateUserMutation()

  const isSuperuser = me?.is_superuser ?? false
  const isPlatformAdmin = !isSuperuser && (me?.roles?.includes("platform.admin") ?? false)
  const isDeptAdmin = !isSuperuser && !isPlatformAdmin
  const canAssignDirect = isSuperuser || isPlatformAdmin

  const form = useForm({
    initialValues: { username: "", first_name: "", last_name: "", email: "", department: "" },
    validate: {
      first_name: (v) => (v.trim() ? null : "First name is required"),
      last_name: (v) => (v.trim() ? null : "Last name is required"),
      email: (v) => (v?.trim() ? null : "Email is required"),
      department: (v) => (isDeptAdmin ? null : v?.trim() ? null : "Department is required"),
    },
  })

  const myDept = useMemo(() => {
    if (!isDeptAdmin || !me?.department || !departments) return null
    return departments.find((d) => d.code === me.department.code) ?? null
  }, [isDeptAdmin, me, departments])

  const selectedDeptId = isDeptAdmin ? (myDept?.id ?? "") : form.values.department
  const selectedDept = departments?.find((d) => d.id === selectedDeptId)
  const hasDepartment = isDeptAdmin ? !!myDept : !!form.values.department

  const { data: formOptions } = useGetRoleFormOptionsQuery(selectedDeptId || undefined, {
    skip: !user || !selectedDeptId,
  })

  const allFormRoles = useMemo((): RoleRef[] => {
    if (!formOptions) return []
    return [
      ...formOptions.management_roles,
      ...Object.values(formOptions.system_roles).flat(),
    ]
  }, [formOptions])

  const computePermissionsForRole = useCallback((roleId: string): string[] => {
    if (!allPermissions || !roleId) return []
    const role = allFormRoles.find((r) => r.id === roleId)
    if (!role?.policies) return []
    const permCodes = new Set<string>()
    role.policies.forEach((p) => p.permission_codes.forEach((c) => permCodes.add(c)))
    return allPermissions.filter((p) => permCodes.has(p.code)).map((p) => p.id)
  }, [allFormRoles, allPermissions])

  const computePermissionsFromRoles = useCallback((
    mgmtRoleCode: string | null,
    sysRoles: Record<string, string>
  ): string[] => {
    if (!allPermissions) return []
    const roleIds = [
      ...(mgmtRoleCode ? [formOptions?.management_roles.find((r) => r.code === mgmtRoleCode)?.id] : []),
      ...Object.values(sysRoles).filter(Boolean),
    ].filter(Boolean) as string[]
    const permCodes = new Set<string>()
    for (const roleId of roleIds) {
      const role = allFormRoles.find((r) => r.id === roleId)
      role?.policies?.forEach((p) => p.permission_codes.forEach((c) => permCodes.add(c)))
    }
    return allPermissions.filter((p) => permCodes.has(p.code)).map((p) => p.id)
  }, [allFormRoles, allPermissions, formOptions])

  useEffect(() => {
    if (!user) return
    form.setValues({
      username: user.username ?? "",
      first_name: user.first_name ?? "",
      last_name: user.last_name ?? "",
      email: user.email ?? "",
      department: user.department?.id ?? "",
    })

    setManagementRole(user.management_role?.code ?? null)
    const sysRoles: Record<string, string> = {}
    user.system_roles.forEach((r) => { sysRoles[r.system] = r.id })
    setSystemRoles(sysRoles)

    if (!initializedRef.current && userDetail && allPermissions) {
      if (isSuperuser || isPlatformAdmin) {
        setSelectedPermissionIds(userDetail.permission_ids)
      }
      initializedRef.current = true
    }
  }, [user, userDetail, allPermissions])

  // Permissions that come from roles — pre-checked but disabled for platform admin
  const rolePermIds = useMemo(() => {
    if (!userDetail || !isPlatformAdmin) return new Set<string>()
    return new Set(userDetail.role_permission_ids)
  }, [userDetail, isPlatformAdmin])

  const selectedMgmtRole = formOptions?.management_roles.find((r) => r.code === managementRole)
  const grantsForCurrentMgmt = selectedMgmtRole?.grants_systems
    ?? (user?.management_role?.code === managementRole ? user.management_role.grants_systems ?? [] : [])

  const allowedSystems = hasDepartment
    ? (grantsForCurrentMgmt.length ? grantsForCurrentMgmt : (selectedDept?.allowed_systems ?? []))
    : []

  const managementRoleOptions = useMemo(() => {
    if (isDeptAdmin || !formOptions) return []
    return [
      { value: "", label: "None" },
      ...formOptions.management_roles.map((r) => ({ value: r.code, label: r.name })),
    ]
  }, [isDeptAdmin, formOptions])

  const getRolesForSystem = (system: string) =>
    formOptions?.system_roles[system] ?? []

  const groupAndSort = (perms: Permission[]): Record<string, Record<string, Permission[]>> => {
    const grouped: Record<string, Record<string, Permission[]>> = {}
    for (const p of perms) {
      if (!grouped[p.system]) grouped[p.system] = {}
      if (!grouped[p.system][p.resource]) grouped[p.system][p.resource] = []
      grouped[p.system][p.resource].push(p)
    }
    for (const system of Object.keys(grouped)) {
      for (const resource of Object.keys(grouped[system])) {
        grouped[system][resource].sort((a, b) => {
          if (a.action === "read") return -1
          if (b.action === "read") return 1
          return a.action.localeCompare(b.action)
        })
      }
    }
    return grouped
  }

  const allPermissionsBySystemResource = useMemo((): Record<string, Record<string, Permission[]>> => {
    if (!allPermissions) return {}
    return groupAndSort(allPermissions)
  }, [allPermissions])

  const togglePermission = (perm: Permission, checkedIds: string[], setter: React.Dispatch<React.SetStateAction<string[]>>) => {
    const isRead = perm.action === "read"
    if (isRead) {
      const isChecked = checkedIds.includes(perm.id)
      if (isChecked) {
        const resourcePermIds = new Set(
          allPermissions?.filter((p) => p.system === perm.system && p.resource === perm.resource).map((p) => p.id) ?? []
        )
        setter((prev) => prev.filter((id) => !resourcePermIds.has(id)))
      } else {
        setter((prev) => [...prev, perm.id])
      }
    } else {
      const readPerm = allPermissions?.find(
        (p) => p.system === perm.system && p.resource === perm.resource && p.action === "read"
      )
      const readChecked = readPerm ? checkedIds.includes(readPerm.id) : false
      if (!readChecked) return
      setter((prev) => prev.includes(perm.id) ? prev.filter((x) => x !== perm.id) : [...prev, perm.id])
    }
  }

  const closeModal = () => {
    onClose()
    setError(null)
    form.reset()
    setManagementRole(null)
    setSystemRoles({})
    setSelectedPermissionIds([])
    setShowExtraPerms(false)
    initializedRef.current = false
  }

  const handleSubmit = async (values: typeof form.values) => {
    if (!user) return
    setError(null)
    const deptId = isDeptAdmin ? (myDept?.id ?? "") : values.department
    if (!deptId) { setError("Department is required"); return }
    const systemRoleIds = Object.values(systemRoles).filter(Boolean)
    const managementRoleId = selectedMgmtRole?.id
      ?? (user?.management_role?.code === managementRole ? user.management_role?.id : null)
      ?? null
    const allRoleIds = [...(managementRoleId ? [managementRoleId] : []), ...systemRoleIds]
    if (allRoleIds.length === 0) { setError("User must have at least one role"); return }
    if (allowedSystems.length > 0 && systemRoleIds.length === 0) { setError("At least one system role is required"); return }
    const finalPermissionIds = isSuperuser
      ? selectedPermissionIds
      : selectedPermissionIds.filter((id) => !rolePermIds.has(id))
    try {
      await updateUser({
        id: user.id,
        body: {
          ...values,
          ...(isSuperuser && values.username ? { username: values.username } : {}),
          department: deptId,
          roles: allRoleIds,
          ...(canAssignDirect && { permission_ids: finalPermissionIds }),
        },
      }).unwrap()
      closeModal()
    } catch (err: any) {
      const data = err?.data
      const fieldError = data?.email?.[0] ?? data?.first_name?.[0] ?? data?.last_name?.[0]
      setError(fieldError ?? data?.detail ?? data?.message ?? "Failed to update user")
    }
  }

  const departmentOptions = departments?.map((d) => ({ value: d.id, label: d.name })) ?? []

  const renderPermissionGroup = (
    bySystemResource: Record<string, Record<string, Permission[]>>,
    checkedIds: string[],
    setter: React.Dispatch<React.SetStateAction<string[]>>,
    disabledIds?: Set<string>
  ) => (
    <>
      {Object.entries(bySystemResource).map(([system, resources]) => (
        <Box key={system}>
          <Text size="xs" fw={700} tt="uppercase" c="dimmed" mb={8}>{system}</Text>
          <Stack gap="xs">
            {Object.entries(resources).map(([resource, perms]) => {
              const readPerm = perms.find((p) => p.action === "read")
              const readChecked = readPerm ? checkedIds.includes(readPerm.id) : false
              return (
                <Paper key={resource} withBorder p="sm">
                  <Text size="xs" fw={600} c="dimmed" mb={6} tt="capitalize">{resource}</Text>
                  <Stack gap={6}>
                    {perms.map((p) => (
                      <Checkbox
                        key={p.id}
                        label={p.action}
                        description={p.code}
                        checked={checkedIds.includes(p.id)}
                        disabled={disabledIds?.has(p.id) || (p.action !== "read" && !readChecked)}
                        onChange={() => togglePermission(p, checkedIds, setter)}
                      />
                    ))}
                  </Stack>
                </Paper>
              )
            })}
          </Stack>
        </Box>
      ))}
    </>
  )

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

          {isSuperuser ? (
            <>
              <TextInput label="Username" {...form.getInputProps("username")} />
              <Alert icon={<IconAlertCircle size={16} />} color="yellow" variant="light">
                Changing the username will invalidate the user's active tokens within 15 minutes.
              </Alert>
            </>
          ) : (
            <TextInput label="Username" value={user?.username ?? ""} disabled />
          )}
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
                  const role = formOptions?.management_roles.find((r) => r.code === val)
                  const grants = role?.grants_systems ?? []
                  const effectiveSystems = grants.length ? grants : (selectedDept?.allowed_systems ?? [])

                  if (grants.length && effectiveSystems.length > 0) {
                    const suffix = val!.endsWith(".admin") ? "admin" : "viewer"
                    const autoSelected: Record<string, string> = {}
                    for (const system of effectiveSystems) {
                      const match = formOptions?.system_roles[system]?.find((r) => r.code === `${system}.${suffix}`)
                      if (match) autoSelected[system] = match.id
                    }
                    setSystemRoles(autoSelected)
                    if (isSuperuser) {
                      setSelectedPermissionIds(computePermissionsFromRoles(val, autoSelected))
                    }
                  } else if (!val) {
                    setSystemRoles({})
                    if (isSuperuser) setSelectedPermissionIds([])
                  } else if (isSuperuser) {
                    setSelectedPermissionIds(computePermissionsFromRoles(val, systemRoles))
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
                        placeholder="Select role"
                        data={getRolesForSystem(system).map((r) => ({ value: r.id, label: r.name }))}
                        value={systemRoles[system] ?? null}
                        onChange={(val) => {
                          const oldRoleId = systemRoles[system] ?? ""
                          const updated = { ...systemRoles, [system]: val ?? "" }
                          setSystemRoles(updated)
                          if (isSuperuser) {
                            const oldPerms = new Set(computePermissionsForRole(oldRoleId))
                            const newPerms = computePermissionsForRole(val ?? "")
                            setSelectedPermissionIds((prev) => {
                              const base = prev.filter((id) => !oldPerms.has(id))
                              const toAdd = newPerms.filter((id) => !base.includes(id))
                              return [...base, ...toAdd]
                            })
                          }
                        }}
                        clearable
                        style={{ flex: 1 }}
                      />
                    </Group>
                  </Paper>
                ))}
              </Stack>
            </>
          )}

          {canAssignDirect && (
            <>
              <Divider />
              <UnstyledButton onClick={() => setShowExtraPerms((v) => !v)}>
                <Group gap={4}>
                  <Text size="sm" fw={500}>Permissions</Text>
                  {showExtraPerms ? <IconChevronUp size={14} /> : <IconChevronDown size={14} />}
                </Group>
              </UnstyledButton>

              <Collapse in={showExtraPerms}>
                <Stack gap="sm" mt="xs">

                  {(isSuperuser || isPlatformAdmin) && (
                    <>
                      <Text size="xs" c="dimmed">
                        {isSuperuser
                          ? "Check/uncheck any permission. Role selections above are presets."
                          : "Greyed permissions are granted by the user's role and cannot be removed here."}
                      </Text>
                      {renderPermissionGroup(
                        allPermissionsBySystemResource,
                        selectedPermissionIds,
                        setSelectedPermissionIds,
                        isPlatformAdmin ? rolePermIds : undefined
                      )}
                    </>
                  )}

                </Stack>
              </Collapse>
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
