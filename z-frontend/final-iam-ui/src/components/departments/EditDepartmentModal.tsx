import { useState, useEffect } from "react"
import { Modal, TextInput, MultiSelect, Stack, Button, Group, Alert } from "@mantine/core"
import { useForm } from "@mantine/form"
import { IconAlertCircle } from "@tabler/icons-react"
import { useUpdateDepartmentMutation, useGetRolesQuery } from "../../services/iamApi"
import type { Department } from "../../types"

const EXCLUDED_SYSTEMS = new Set(["iam", "dept", "platform"])

interface Props {
  department: Department | null
  onClose: () => void
}

export default function EditDepartmentModal({ department, onClose }: Props) {
  const [error, setError] = useState<string | null>(null)
  const [updateDepartment, { isLoading }] = useUpdateDepartmentMutation()
  const { data: roles } = useGetRolesQuery()

  const availableSystems = [
    ...new Set(
      roles
        ?.map((r) => r.system)
        .filter((s) => typeof s === "string" && s.length > 0 && !EXCLUDED_SYSTEMS.has(s)) ?? []
    ),
  ].map((s) => ({ value: s, label: s.charAt(0).toUpperCase() + s.slice(1) }))

  const form = useForm({
    initialValues: { name: "", allowed_systems: [] as string[] },
    validate: {
      name: (v) => (v.trim() ? null : "Name is required"),
      allowed_systems: (v) => (v.length > 0 ? null : "At least one system is required"),
    },
  })

  useEffect(() => {
    if (!department) return
    form.setValues({
      name: department.name,
      allowed_systems: department.allowed_systems,
    })
  }, [department])

  const handleClose = () => {
    onClose()
    setError(null)
    form.reset()
  }

  const handleSubmit = async (values: typeof form.values) => {
    if (!department) return
    setError(null)
    try {
      await updateDepartment({
        id: department.id,
        body: {
          name: values.name.trim(),
          allowed_systems: values.allowed_systems,
        },
      }).unwrap()
      handleClose()
    } catch (err: any) {
      const data = err?.data
      setError(data?.name?.[0] ?? data?.detail ?? "Failed to update department.")
    }
  }

  return (
    <Modal opened={!!department} onClose={handleClose} title={`Edit — ${department?.code}`}>
      {error && (
        <Alert icon={<IconAlertCircle size={16} />} color="red" mb="md">
          {error}
        </Alert>
      )}
      <form onSubmit={form.onSubmit(handleSubmit)}>
        <Stack gap="md">
          <TextInput
            required
            label="Name"
            {...form.getInputProps("name")}
          />
          <MultiSelect
            label="Allowed Systems"
            placeholder="Select systems"
            data={availableSystems}
            {...form.getInputProps("allowed_systems")}
          />
          <Group justify="flex-end">
            <Button variant="default" onClick={handleClose}>Cancel</Button>
            <Button type="submit" loading={isLoading}>Save</Button>
          </Group>
        </Stack>
      </form>
    </Modal>
  )
}
