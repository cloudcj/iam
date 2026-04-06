import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Center,
  Paper,
  Title,
  Text,
  PasswordInput,
  Button,
  Alert,
  Stack,
} from '@mantine/core'
import { useForm } from '@mantine/form'
import { IconAlertCircle, IconLock } from '@tabler/icons-react'
import { useChangePasswordMutation } from '../services/iamApi'

export default function ChangePasswordPage() {
  const navigate = useNavigate()
  const [changePassword, { isLoading }] = useChangePasswordMutation()
  const [error, setError] = useState<string | null>(null)

  const form = useForm({
    initialValues: {
      current_password: '',
      new_password: '',
      confirm_password: '',
    },
    validate: {
      current_password: (v) => (v.trim() ? null : 'Current password is required'),
      new_password: (v) => (v.length >= 8 ? null : 'Password must be at least 8 characters'),
      confirm_password: (v, values) =>
        v === values.new_password ? null : 'Passwords do not match',
    },
  })

  const handleSubmit = async (values: typeof form.values) => {
    setError(null)
    try {
      await changePassword(values).unwrap()
      navigate('/')
    } catch (err: any) {
      const data = err?.data
      setError(
        data?.current_password?.[0] ??
        data?.new_password?.[0] ??
        data?.confirm_password?.[0] ??
        data?.detail ??
        'Failed to change password'
      )
    }
  }

  return (
    <Center h="100vh" bg="gray.0">
      <Paper w={420} p="xl" radius="md" withBorder shadow="sm">
        <Stack gap="xs" mb="lg">
          <Title order={2}>Change Your Password</Title>
          <Text c="dimmed" size="sm">
            Your account requires a password change before you can continue.
          </Text>
        </Stack>

        {error && (
          <Alert icon={<IconAlertCircle size={16} />} color="red" mb="md">
            {error}
          </Alert>
        )}

        <form onSubmit={form.onSubmit(handleSubmit)}>
          <Stack gap="md">
            <PasswordInput
              label="Current Password"
              placeholder="Enter your current password"
              leftSection={<IconLock size={16} />}
              {...form.getInputProps('current_password')}
            />
            <PasswordInput
              label="New Password"
              placeholder="At least 8 characters"
              leftSection={<IconLock size={16} />}
              {...form.getInputProps('new_password')}
            />
            <PasswordInput
              label="Confirm New Password"
              placeholder="Repeat new password"
              leftSection={<IconLock size={16} />}
              {...form.getInputProps('confirm_password')}
            />
            <Button type="submit" fullWidth loading={isLoading} mt="xs">
              Change Password
            </Button>
          </Stack>
        </form>
      </Paper>
    </Center>
  )
}
