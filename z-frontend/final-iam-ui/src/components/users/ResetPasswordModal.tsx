import { Modal, PasswordInput, Button, Stack, Alert, Group, Text } from '@mantine/core'
import { useForm } from '@mantine/form'
import { IconAlertCircle } from '@tabler/icons-react'
import { useState } from 'react'
import { useResetUserPasswordMutation } from '../../services/iamApi'
import type { User } from '../../types'

interface Props {
  user: User | null
  onClose: () => void
}

export default function ResetPasswordModal({ user, onClose }: Props) {
  const [error, setError] = useState<string | null>(null)
  const [resetPassword, { isLoading }] = useResetUserPasswordMutation()

  const form = useForm({
    initialValues: { new_password: '', confirm_password: '' },
    validate: {
      new_password: (v) => (v.length >= 8 ? null : 'Password must be at least 8 characters'),
      confirm_password: (v, values) => (v === values.new_password ? null : 'Passwords do not match'),
    },
  })

  const handleClose = () => {
    form.reset()
    setError(null)
    onClose()
  }

  const handleSubmit = async (values: typeof form.values) => {
    if (!user) return
    setError(null)
    try {
      await resetPassword({ id: user.id, body: values }).unwrap()
      handleClose()
    } catch (err: any) {
      const data = err?.data
      setError(data?.detail ?? data?.new_password?.[0] ?? 'Failed to reset password')
    }
  }

  return (
    <Modal opened={!!user} onClose={handleClose} title={
      <Text fw={600}>Reset Password — {user?.username}</Text>
    }>
      {error && <Alert icon={<IconAlertCircle size={16} />} color="red" mb="md">{error}</Alert>}
      <form onSubmit={form.onSubmit(handleSubmit)}>
        <Stack gap="sm">
          <PasswordInput required label="New Password" {...form.getInputProps('new_password')} />
          <PasswordInput required label="Confirm Password" {...form.getInputProps('confirm_password')} />
          <Group justify="flex-end" mt="xs">
            <Button variant="default" onClick={handleClose}>Cancel</Button>
            <Button type="submit" loading={isLoading} color="orange">Reset Password</Button>
          </Group>
        </Stack>
      </form>
    </Modal>
  )
}
