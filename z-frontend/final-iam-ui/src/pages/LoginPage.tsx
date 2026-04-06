import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Center,
  Paper,
  Title,
  Text,
  TextInput,
  PasswordInput,
  Button,
  Alert,
  Stack,
} from '@mantine/core'
import { useForm } from '@mantine/form'
import { IconAlertCircle } from '@tabler/icons-react'
import { useLoginMutation } from '../services/iamApi'

export default function LoginPage() {
  const navigate = useNavigate()
  const [login, { isLoading }] = useLoginMutation()
  const [error, setError] = useState<string | null>(null)

  const form = useForm({
    initialValues: { username: '', password: '' },
    validate: {
      username: (v) => (v.trim() ? null : 'Username is required'),
      password: (v) => (v.trim() ? null : 'Password is required'),
    },
  })

  const handleSubmit = async (values: typeof form.values) => {
    setError(null)
    try {
      const result = await login(values).unwrap()
      if (result.must_change_password) {
        navigate('/change-password')
      } else {
        navigate('/')
      }
    } catch (err: any) {
      setError(err?.data?.message ?? err?.data?.detail ?? 'Invalid credentials')
    }
  }

  return (
    <Center h="100vh" bg="gray.0">
      <Paper w={400} p="xl" radius="md" withBorder shadow="sm">
        <Stack gap="xs" mb="lg">
          <Title order={2}>GAIA Admin</Title>
          <Text c="dimmed" size="sm">Sign in to your account</Text>
        </Stack>

        {error && (
          <Alert icon={<IconAlertCircle size={16} />} color="red" mb="md">
            {error}
          </Alert>
        )}

        <form onSubmit={form.onSubmit(handleSubmit)}>
          <Stack gap="md">
            <TextInput
              label="Username"
              placeholder="Enter your username"
              {...form.getInputProps('username')}
            />
            <PasswordInput
              label="Password"
              placeholder="Enter your password"
              {...form.getInputProps('password')}
            />
            <Button type="submit" fullWidth loading={isLoading} mt="xs">
              Sign in
            </Button>
          </Stack>
        </form>
      </Paper>
    </Center>
  )
}
