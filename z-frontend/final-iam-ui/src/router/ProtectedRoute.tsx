// import { Navigate } from 'react-router-dom'
// import { useGetMeQuery } from '../services/iamApi'
// import { Center, Loader } from '@mantine/core'

// export default function ProtectedRoute({ children }: { children: React.ReactNode }) {
//   const { data: me, isLoading, isFetching } = useGetMeQuery()

//   if (isLoading || isFetching) return <Center h="100vh"><Loader /></Center>
//   if (!me) return <Navigate to="/login" replace />

//   return <>{children}</>
// }
import { Navigate, useNavigate } from 'react-router-dom'
import { useGetMeQuery } from '../services/iamApi'
import { Center, Loader, Stack, Title, Text, ThemeIcon, Button } from '@mantine/core'
import { IconShieldOff } from '@tabler/icons-react'
import { useLogoutMutation } from '../services/iamApi'

function AccessDenied() {
  const [logout] = useLogoutMutation()
  const navigate = useNavigate()

  const handleLogout = async () => {
    await logout()
    navigate('/login', { replace: true })
  }

  return (
    <Center h="100vh">
      <Stack align="center" gap="md">
        <ThemeIcon size={64} radius="xl" color="red" variant="light">
          <IconShieldOff size={36} />
        </ThemeIcon>
        <Title order={3}>Access Denied</Title>
        <Text c="dimmed" ta="center" maw={360}>
          Your account does not have permission to access the IAM Admin panel.
          Contact your administrator.
        </Text>
        <Button variant="default" onClick={handleLogout}>
          Sign out
        </Button>
      </Stack>
    </Center>
  )
}

export default function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { data: me, isLoading, isFetching } = useGetMeQuery()

  if (isLoading || isFetching) return <Center h="100vh"><Loader /></Center>
  if (!me) return <Navigate to="/login" replace />

  const hasIamAccess = me.is_superuser || me.permissions.includes('iam.user.read')
  if (!hasIamAccess) return <AccessDenied />

  return <>{children}</>
}
