import { Modal, Stack, Group, Text, Badge, Divider, Avatar } from "@mantine/core"
import type { User } from "../../types"

interface Props {
  user: User | null
  onClose: () => void
}

export default function ViewUserModal({ user, onClose }: Props) {
  if (!user) return null

  return (
    <Modal opened={!!user} onClose={onClose} title="User Details" size="md">
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
          {user.roles.map((role) => (
            <Badge key={role} size="sm" variant="light" tt="none">{role}</Badge>
          ))}
        </Group>
      </Stack>
    </Modal>
  )
}
