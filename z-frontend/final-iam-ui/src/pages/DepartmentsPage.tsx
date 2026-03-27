import { useState } from "react"
import { Title, Button, Badge, Group, ActionIcon } from "@mantine/core"
import { DataTable } from "mantine-datatable"
import { IconPlus, IconEdit, IconTrash } from "@tabler/icons-react"
import Swal from "sweetalert2"
import {
  useGetDepartmentsQuery,
  useGetMeQuery,
  useDeleteDepartmentMutation,
} from "../services/iamApi"
import CreateDepartmentModal from "../components/departments/CreateDepartmentModal"
import EditDepartmentModal from "../components/departments/EditDepartmentModal"
import type { Department } from "../types"

export default function DepartmentsPage() {
  const [createOpened, setCreateOpened] = useState(false)
  const [editDept, setEditDept] = useState<Department | null>(null)

  const { data: departments, isLoading } = useGetDepartmentsQuery()
  const { data: me } = useGetMeQuery()
  const [deleteDepartment] = useDeleteDepartmentMutation()

  const canCreate = me?.is_superuser || me?.permissions.includes("iam.department.create")
  const canEdit   = me?.is_superuser || me?.permissions.includes("iam.department.update")
  const canDelete = me?.is_superuser || me?.permissions.includes("iam.department.delete")

  const handleDelete = async (dept: Department) => {
    const result = await Swal.fire({
      title: `Delete ${dept.name}?`,
      text: "This action cannot be undone. Users in this department must be reassigned first.",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#e03131",
      cancelButtonColor: "#868e96",
      confirmButtonText: "Yes, delete",
      cancelButtonText: "Cancel",
    })

    if (result.isConfirmed) {
      try {
        await deleteDepartment(dept.id).unwrap()
        Swal.fire({ title: "Deleted", icon: "success", timer: 1500, showConfirmButton: false })
      } catch (err: any) {
        Swal.fire("Error", err?.data?.detail ?? "Failed to delete department.", "error")
      }
    }
  }

  return (
    <>
      <Group justify="space-between" mb="lg">
        <Title order={3}>Departments</Title>
        {canCreate && (
          <Button leftSection={<IconPlus size={16} />} onClick={() => setCreateOpened(true)}>
            Create Department
          </Button>
        )}
      </Group>

      <DataTable
        withTableBorder
        withColumnBorders
        striped
        highlightOnHover
        fetching={isLoading}
        minHeight={departments && departments.length > 0 ? undefined : 150}
        noRecordsText="No departments found"
        records={departments ?? []}
        idAccessor="id"
        columns={[
          {
            accessor: "name",
            title: "Name",
            resizable: true,
          },
          {
            accessor: "allowed_systems",
            title: "Allowed Systems",
            resizable: true,
            render: (dept) =>
              dept.allowed_systems.length > 0 ? (
                <Group gap={4}>
                  {dept.allowed_systems.map((s) => (
                    <Badge key={s} size="sm" variant="light" tt="none">
                      {s}
                    </Badge>
                  ))}
                </Group>
              ) : (
                "—"
              ),
          },
          {
            accessor: "actions",
            title: "Row Actions",
            textAlign: "right",
            render: (dept) => (
              <Group gap={4} justify="flex-end">
                {canEdit && (dept.code !== "GLOBAL" || me?.is_superuser) && (
                  <ActionIcon
                    size="sm"
                    variant="subtle"
                    color="blue"
                    onClick={() => setEditDept(dept)}
                  >
                    <IconEdit size={16} />
                  </ActionIcon>
                )}
                {canDelete && dept.code !== "GLOBAL" && (
                  <ActionIcon
                    size="sm"
                    variant="subtle"
                    color="red"
                    onClick={() => handleDelete(dept)}
                  >
                    <IconTrash size={16} />
                  </ActionIcon>
                )}
              </Group>
            ),
          },
        ]}
      />

      <CreateDepartmentModal
        opened={createOpened}
        onClose={() => setCreateOpened(false)}
      />
      <EditDepartmentModal
        department={editDept}
        onClose={() => setEditDept(null)}
      />
    </>
  )
}
