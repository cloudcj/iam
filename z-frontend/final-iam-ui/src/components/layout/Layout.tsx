import { AppShell, NavLink, Text, Group, Box } from '@mantine/core'
import { Outlet, useNavigate, useLocation } from 'react-router-dom'
import {
  IconDashboard,
  IconUsers,
  IconShield,
  IconKey,
  IconBuilding,
  IconLogout,
} from '@tabler/icons-react'
import { useLogoutMutation } from '../../services/iamApi'

const navItems = [
  { label: 'Dashboard', icon: IconDashboard, path: '/' },
  { label: 'Users', icon: IconUsers, path: '/users' },
  { label: 'Roles', icon: IconShield, path: '/roles' },
  { label: 'Permissions', icon: IconKey, path: '/permissions' },
  { label: 'Departments', icon: IconBuilding, path: '/departments' },
]

export default function Layout() {
  const navigate = useNavigate()
  const location = useLocation()
  const [logout] = useLogoutMutation()

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  return (
    <AppShell navbar={{ width: 240, breakpoint: 'sm' }} padding="md">
      <AppShell.Navbar p="md">
        <Box mb="lg">
          <Text fw={700} size="lg">IAM Admin</Text>
        </Box>
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            label={item.label}
            leftSection={<item.icon size={18} />}
            active={location.pathname === item.path}
            onClick={() => navigate(item.path)}
            mb={4}
          />
        ))}
        <Box mt="auto">
          <NavLink
            label="Logout"
            leftSection={<IconLogout size={18} />}
            onClick={handleLogout}
            color="red"
          />
        </Box>
      </AppShell.Navbar>
      <AppShell.Main>
        <Outlet />
      </AppShell.Main>
    </AppShell>
  )
}
