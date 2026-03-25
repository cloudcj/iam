import { useState } from "react";
import { Title, Button, Badge, Group } from "@mantine/core";
import { DataTable } from "mantine-datatable";
import { IconPlus } from "@tabler/icons-react";
import { useGetUsersQuery, useGetMeQuery } from "../services/iamApi";
import CreateUserModal from "../components/users/CreateUserModal";

export default function UsersPage() {
  const [opened, setOpened] = useState(false);
  const { data: users, isLoading } = useGetUsersQuery();
  const { data: me } = useGetMeQuery();

  const canCreate = me?.is_superuser || me?.permissions.includes("iam.user.create");

  return (
    <>
      <Group justify="space-between" mb="lg">
        <Title order={3}>Users</Title>
        {canCreate && (
          <Button leftSection={<IconPlus size={16} />} onClick={() => setOpened(true)}>
            Create User
          </Button>
        )}
      </Group>

      <DataTable
        withTableBorder
        withColumnBorders
        striped
        highlightOnHover
        fetching={isLoading}
        records={users ?? []}
        idAccessor="id"
        columns={[
          {
            accessor: "username",
            title: "Username",
            resizable: true,
            render: (user) => <strong>{user.username}</strong>,
          },
          {
            accessor: "email",
            title: "Email",
            resizable: true,
            render: (user) => user.email || "—",
          },
          {
            accessor: "department",
            title: "Department",
            resizable: true,
            render: (user) => user.department?.name ?? "—",
          },
          {
            accessor: "roles",
            title: "Roles",
            render: (user) => {
              const visible = user.roles.slice(0, 2)
              const rest = user.roles.length - 2
              return (
                <Group gap={4}>
                  {visible.map((role) => (
                    <Badge key={role} size="sm" variant="light" tt="none">
                      {role}
                    </Badge>
                  ))}
                  {rest > 0 && (
                    <Badge size="sm" variant="outline" color="gray">
                      +{rest} more
                    </Badge>
                  )}
                </Group>
              )
            },
          },
          {
            accessor: "is_active",
            title: "Status",
            resizable: true,
            render: (user) => (
              <Badge color={user.is_active ? "green" : "red"} size="sm">
                {user.is_active ? "Active" : "Inactive"}
              </Badge>
            ),
          },
        ]}
        storeColumnsKey="users-table"
      />

      <CreateUserModal opened={opened} onClose={() => setOpened(false)} />
    </>
  );
}
