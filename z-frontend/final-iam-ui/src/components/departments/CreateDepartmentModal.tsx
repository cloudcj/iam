import { useState } from "react"
import { Modal, TextInput, MultiSelect, Stack, Button, Group, Alert } from "@mantine/core"
import { useForm } from "@mantine/form"
import { IconAlertCircle } from "@tabler/icons-react"
import { useCreateDepartmentMutation, useGetRolesQuery } from "../../services/iamApi"

const EXCLUDED_SYSTEMS = new Set(["iam", "dept", "platform"])

interface Props {
  opened: boolean
  onClose: () => void
}

export default function CreateDepartmentModal({ opened, onClose }: Props) {
  const [error, setError] = useState<string | null>(null)
  const [createDepartment, { isLoading }] = useCreateDepartmentMutation()
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

  const handleClose = () => {
    onClose()
    setError(null)
    form.reset()
  }

  const handleSubmit = async (values: typeof form.values) => {
    setError(null)
    try {
      await createDepartment({
        name: values.name.trim(),
        allowed_systems: values.allowed_systems,
      }).unwrap()
      handleClose()
    } catch (err: any) {
      const data = err?.data
      const fieldError = data?.name?.[0] ?? data?.code?.[0]
      setError(fieldError ?? data?.detail ?? "Failed to create department.")
    }
  }

  return (
    <Modal opened={opened} onClose={handleClose} title="Create Department">
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
            placeholder="Engineering"
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
            <Button type="submit" loading={isLoading}>Create</Button>
          </Group>
        </Stack>
      </form>
    </Modal>
  )
}
