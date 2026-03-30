import { useState } from "react";
import { Title, Button, Badge, Group, ActionIcon } from "@mantine/core";
import { DataTable } from "mantine-datatable";
import { IconPlus, IconEye, IconEdit, IconTrash } from "@tabler/icons-react";
import Swal from "sweetalert2";
import {
  useGetUsersQuery,
  useGetMeQuery,
  useDeleteUserMutation,
} from "../services/iamApi";
import CreateUserModal from "../components/users/CreateUserModal";
import ViewUserModal from "../components/users/ViewUserModal";
import EditUserModal from "../components/users/EditUserModal";
import type { User } from "../types";

export default function UsersPage() {
  const [createOpened, setCreateOpened] = useState(false);
  const [viewUser, setViewUser] = useState<User | null>(null);
  const [editUser, setEditUser] = useState<User | null>(null);

  const { data: users, isLoading } = useGetUsersQuery();
  const { data: me } = useGetMeQuery();
  const [deleteUser] = useDeleteUserMutation();

  const canCreate =
    me?.is_superuser || me?.permissions.includes("iam.user.create");
  const canEdit =
    me?.is_superuser || me?.permissions.includes("iam.user.update");
  const canDelete =
    me?.is_superuser || me?.permissions.includes("iam.user.delete");

  const handleDelete = async (user: User) => {
    const result = await Swal.fire({
      title: `Delete ${user.username}?`,
      text: "This action cannot be undone.",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#e03131",
      cancelButtonColor: "#868e96",
      confirmButtonText: "Yes, delete",
      cancelButtonText: "Cancel",
    });

    if (result.isConfirmed) {
      try {
        await deleteUser(user.id).unwrap();
        Swal.fire({
          title: "Deleted",
          text: `${user.username} has been deactivated.`,
          icon: "success",
          timer: 1500,
          showConfirmButton: false,
        });
      } catch (err: any) {
        Swal.fire(
          "Error",
          err?.data?.detail ?? "Failed to delete user.",
          "error",
        );
      }
    }
  };

  return (
    <>
      <Group justify="space-between" mb="lg">
        <Title order={3}>Users</Title>
        {canCreate && (
          <Button
            leftSection={<IconPlus size={16} />}
            onClick={() => setCreateOpened(true)}
          >
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
        minHeight={users && users.length > 0 ? undefined : 150}
        noRecordsText="No users found"
        records={users ?? []}
        idAccessor="id"
        storeColumnsKey="users-table"
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
            resizable: true,
            render: (user) => {
              const allRoles = [
                ...(user.management_role ? [user.management_role] : []),
                ...user.system_roles,
              ]
              const visible = allRoles.slice(0, 2)
              const rest = allRoles.length - 2
              return (
                <Group gap={4}>
                  {visible.map((role) => (
                    <Badge key={role.id} size="sm" variant="light" tt="none">
                      {role.name}
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
                {user.is_active ? "Active" : "Deactivated"}
              </Badge>
            ),
          },
          {
            accessor: "actions",
            title: "Row Actions",
            textAlign: "right",
            render: (user) => (
              <Group gap={4} justify="flex-end">
                <ActionIcon
                  size="sm"
                  variant="subtle"
                  color="teal"
                  onClick={() => setViewUser(user)}
                >
                  <IconEye size={16} />
                </ActionIcon>
                {canEdit && (
                  <ActionIcon
                    size="sm"
                    variant="subtle"
                    color="blue"
                    onClick={() => setEditUser(user)}
                  >
                    <IconEdit size={16} />
                  </ActionIcon>
                )}
                {canDelete && (
                  <ActionIcon
                    size="sm"
                    variant="subtle"
                    color="red"
                    onClick={() => handleDelete(user)}
                  >
                    <IconTrash size={16} />
                  </ActionIcon>
                )}
              </Group>
            ),
          },
        ]}
      />

      <CreateUserModal
        opened={createOpened}
        onClose={() => setCreateOpened(false)}
      />
      <ViewUserModal user={viewUser} onClose={() => setViewUser(null)} />
      <EditUserModal user={editUser} onClose={() => setEditUser(null)} />
    </>
  );
}
