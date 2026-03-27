import { Box, Title, TextInput, Button, Stack, Alert, PasswordInput, Text, Group, Card } from '@mantine/core'
import { useForm } from '@mantine/form'
import { IconAlertCircle, IconCheck, IconPencil, IconX } from '@tabler/icons-react'
import { useState, useEffect } from 'react'
import { useGetMeQuery, useUpdateProfileMutation, useChangePasswordMutation } from '../services/iamApi'

export default function ProfilePage() {
  const { data: me } = useGetMeQuery()
  const [updateProfile, { isLoading: profileLoading }] = useUpdateProfileMutation()
  const [changePassword, { isLoading: passwordLoading }] = useChangePasswordMutation()

  const [editingProfile, setEditingProfile] = useState(false)
  const [showChangePassword, setShowChangePassword] = useState(false)
  const [profileError, setProfileError] = useState<string | null>(null)
  const [profileSuccess, setProfileSuccess] = useState(false)
  const [passwordError, setPasswordError] = useState<string | null>(null)
  const [passwordSuccess, setPasswordSuccess] = useState(false)

  const profileForm = useForm({
    initialValues: { first_name: '', last_name: '', email: '' },
    validate: {
      first_name: (v) => (v.trim() ? null : 'First name is required'),
      last_name: (v) => (v.trim() ? null : 'Last name is required'),
      email: (v) => (v.trim() ? null : 'Email is required'),
    },
  })

  const passwordForm = useForm({
    initialValues: { current_password: '', new_password: '', confirm_password: '' },
    validate: {
      current_password: (v) => (v ? null : 'Current password is required'),
      new_password: (v) => (v.length >= 8 ? null : 'Password must be at least 8 characters'),
      confirm_password: (v, values) => (v === values.new_password ? null : 'Passwords do not match'),
    },
  })

  useEffect(() => {
    if (me) {
      profileForm.setValues({
        first_name: me.first_name ?? '',
        last_name: me.last_name ?? '',
        email: me.email ?? '',
      })
    }
  }, [me])

  const handleEditClick = () => {
    profileForm.setValues({
      first_name: me?.first_name ?? '',
      last_name: me?.last_name ?? '',
      email: me?.email ?? '',
    })
    setProfileError(null)
    setProfileSuccess(false)
    setEditingProfile(true)
  }

  const handleCancelEdit = () => {
    setEditingProfile(false)
    setProfileError(null)
  }

  const handleProfileSubmit = async (values: typeof profileForm.values) => {
    setProfileError(null)
    setProfileSuccess(false)
    try {
      await updateProfile(values).unwrap()
      setProfileSuccess(true)
      setEditingProfile(false)
    } catch (err: any) {
      const data = err?.data
      setProfileError(data?.email?.[0] ?? data?.detail ?? 'Failed to update profile')
    }
  }

  const handleCancelPassword = () => {
    setShowChangePassword(false)
    setPasswordError(null)
    setPasswordSuccess(false)
    passwordForm.reset()
  }

  const handlePasswordSubmit = async (values: typeof passwordForm.values) => {
    setPasswordError(null)
    setPasswordSuccess(false)
    try {
      await changePassword(values).unwrap()
      setPasswordSuccess(true)
      setShowChangePassword(false)
      passwordForm.reset()
    } catch (err: any) {
      const data = err?.data
      setPasswordError(data?.current_password?.[0] ?? data?.detail ?? 'Failed to change password')
    }
  }

  return (
    <Box maw={560}>
      <Title order={2} mb="xs">Profile</Title>
      <Text c="dimmed" size="sm" mb="xl">Manage your personal information and password.</Text>

      {/* Personal Information */}
      <Card withBorder p="lg" mb="xl" radius="md">
        <Group justify="space-between" mb="md">
          <Title order={4}>Personal Information</Title>
          {!editingProfile && (
            <Button size="xs" variant="default" leftSection={<IconPencil size={14} />} onClick={handleEditClick}>
              Edit
            </Button>
          )}
        </Group>

        {profileSuccess && !editingProfile && (
          <Alert icon={<IconCheck size={16} />} color="green" mb="md">Profile updated successfully.</Alert>
        )}

        {!editingProfile ? (
          <Stack gap="sm">
            <Box>
              <Text size="xs" c="dimmed">Username</Text>
              <Text fw={500}>{me?.username}</Text>
            </Box>
            <Group grow>
              <Box>
                <Text size="xs" c="dimmed">First Name</Text>
                <Text fw={500}>{me?.first_name}</Text>
              </Box>
              <Box>
                <Text size="xs" c="dimmed">Last Name</Text>
                <Text fw={500}>{me?.last_name}</Text>
              </Box>
            </Group>
            <Box>
              <Text size="xs" c="dimmed">Email</Text>
              <Text fw={500}>{me?.email}</Text>
            </Box>
            <Box>
              <Text size="xs" c="dimmed">Department</Text>
              <Text fw={500}>{me?.department?.name ?? '—'}</Text>
            </Box>
          </Stack>
        ) : (
          <form onSubmit={profileForm.onSubmit(handleProfileSubmit)}>
            {profileError && <Alert icon={<IconAlertCircle size={16} />} color="red" mb="md">{profileError}</Alert>}
            <Stack gap="sm">
              <Group grow>
                <TextInput required label="First Name" {...profileForm.getInputProps('first_name')} />
                <TextInput required label="Last Name" {...profileForm.getInputProps('last_name')} />
              </Group>
              <TextInput required label="Email" {...profileForm.getInputProps('email')} />
              <Group mt="xs">
                <Button type="submit" loading={profileLoading}>Save Changes</Button>
                <Button variant="default" leftSection={<IconX size={14} />} onClick={handleCancelEdit}>Cancel</Button>
              </Group>
            </Stack>
          </form>
        )}
      </Card>

      {/* Change Password */}
      <Card withBorder p="lg" radius="md">
        <Group justify="space-between" mb="md">
          <Title order={4}>Password</Title>
          {!showChangePassword && (
            <Button size="xs" variant="default" leftSection={<IconPencil size={14} />} onClick={() => setShowChangePassword(true)}>
              Change Password
            </Button>
          )}
        </Group>

        {passwordSuccess && !showChangePassword && (
          <Alert icon={<IconCheck size={16} />} color="green">Password changed successfully.</Alert>
        )}

        {!showChangePassword ? (
          <Text size="sm" c="dimmed">••••••••</Text>
        ) : (
          <form onSubmit={passwordForm.onSubmit(handlePasswordSubmit)}>
            {passwordError && <Alert icon={<IconAlertCircle size={16} />} color="red" mb="md">{passwordError}</Alert>}
            <Stack gap="sm">
              <PasswordInput required label="Current Password" {...passwordForm.getInputProps('current_password')} />
              <PasswordInput required label="New Password" {...passwordForm.getInputProps('new_password')} />
              <PasswordInput required label="Confirm New Password" {...passwordForm.getInputProps('confirm_password')} />
              <Group mt="xs">
                <Button type="submit" loading={passwordLoading}>Change Password</Button>
                <Button variant="default" leftSection={<IconX size={14} />} onClick={handleCancelPassword}>Cancel</Button>
              </Group>
            </Stack>
          </form>
        )}
      </Card>
    </Box>
  )
}
