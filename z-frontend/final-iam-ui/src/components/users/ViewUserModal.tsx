import { Modal, Stack, Group, Text, Badge, Divider, Avatar, Button, PasswordInput, Alert } from "@mantine/core"
import { useForm } from "@mantine/form"
import { IconAlertCircle, IconKey, IconX } from "@tabler/icons-react"
import { useState } from "react"
import type { User } from "../../types"
import { useGetMeQuery, useResetUserPasswordMutation } from "../../services/iamApi"

interface Props {
  user: User | null
  onClose: () => void
}

export default function ViewUserModal({ user, onClose }: Props) {
  const { data: me } = useGetMeQuery()
  const [resetPassword, { isLoading }] = useResetUserPasswordMutation()
  const [showReset, setShowReset] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const canResetPassword = me?.is_superuser || me?.permissions?.includes("iam.user.reset_password")

  const form = useForm({
    initialValues: { new_password: "", confirm_password: "" },
    validate: {
      new_password: (v) => (v.length >= 8 ? null : "Password must be at least 8 characters"),
      confirm_password: (v, values) => (v === values.new_password ? null : "Passwords do not match"),
    },
  })

  const handleClose = () => {
    form.reset()
    setError(null)
    setShowReset(false)
    onClose()
  }

  const handleResetSubmit = async (values: typeof form.values) => {
    if (!user) return
    setError(null)
    try {
      await resetPassword({ id: user.id, body: values }).unwrap()
      form.reset()
      setShowReset(false)
    } catch (err: any) {
      const data = err?.data
      setError(data?.detail ?? data?.new_password?.[0] ?? "Failed to reset password")
    }
  }

  if (!user) return null

  return (
    <Modal opened={!!user} onClose={handleClose} title="User Details" size="md">
      <Stack gap="md">
        <Group>
          <Avatar size="lg" radius="xl" color="blue">
            {user.first_name?.[0] || user.username[0].toUpperCase()}
          </Avatar>
          <Stack gap={2}>
            <Text fw={600} size="lg">{user.first_name} {user.last_name}</Text>
            <Text c="dimmed" size="sm">@{user.username}</Text>
          </Stack>
        </Group>

        <Divider />

        <Group justify="space-between">
          <Text size="sm" c="dimmed">Email</Text>
          <Text size="sm">{user.email || "—"}</Text>
        </Group>
        <Group justify="space-between">
          <Text size="sm" c="dimmed">Department</Text>
          <Text size="sm">{user.department?.name ?? "—"}</Text>
        </Group>
        <Group justify="space-between">
          <Text size="sm" c="dimmed">Status</Text>
          <Badge color={user.is_active ? "green" : "red"} size="sm">
            {user.is_active ? "Active" : "Inactive"}
          </Badge>
        </Group>

        <Divider label="Roles" labelPosition="left" />
        <Group gap={6}>
          {user.management_role && (
            <Badge key={user.management_role.id} size="sm" variant="light" color="violet" tt="none">
              {user.management_role.name}
            </Badge>
          )}
          {user.system_roles.map((role) => (
            <Badge key={role.id} size="sm" variant="light" tt="none">{role.name}</Badge>
          ))}
        </Group>

        {canResetPassword && (
          <>
            <Divider label="Admin Actions" labelPosition="left" />
            {!showReset ? (
              <Button
                size="xs"
                variant="light"
                color="orange"
                leftSection={<IconKey size={14} />}
                onClick={() => setShowReset(true)}
                w="fit-content"
              >
                Reset Password
              </Button>
            ) : (
              <form onSubmit={form.onSubmit(handleResetSubmit)}>
                <Stack gap="sm">
                  {error && <Alert icon={<IconAlertCircle size={16} />} color="red">{error}</Alert>}
                  <PasswordInput required label="New Password" {...form.getInputProps("new_password")} />
                  <PasswordInput required label="Confirm Password" {...form.getInputProps("confirm_password")} />
                  <Group>
                    <Button type="submit" size="xs" color="orange" loading={isLoading}>Reset Password</Button>
                    <Button size="xs" variant="default" leftSection={<IconX size={12} />} onClick={() => { setShowReset(false); setError(null); form.reset() }}>Cancel</Button>
                  </Group>
                </Stack>
              </form>
            )}
          </>
        )}
      </Stack>
    </Modal>
  )
}
