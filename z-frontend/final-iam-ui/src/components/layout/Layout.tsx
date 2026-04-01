import { AppShell, NavLink, Text, Box, Divider } from '@mantine/core'
import { Outlet, useNavigate, useLocation } from 'react-router-dom'
import {
  IconDashboard,
  IconUsers,
  IconBuilding,
  IconLogout,
  IconClipboardCheck,
  IconUserCircle,
  IconShieldCheck,
  IconServer,
  IconMap,
  IconLayoutGrid,
  IconDevices,
} from '@tabler/icons-react'
import { useLogoutMutation } from '../../services/iamApi'

const iamNavItems = [
  { label: 'Dashboard', icon: IconDashboard, path: '/' },
  { label: 'Users', icon: IconUsers, path: '/users' },
  { label: 'Departments', icon: IconBuilding, path: '/departments' },
  { label: 'Approval Management', icon: IconClipboardCheck, path: '/approvals' },
  { label: 'Profile', icon: IconUserCircle, path: '/profile' },
  { label: 'Audit Logs', icon: IconShieldCheck, path: '/audit' },
]

const troposNavItems = [
  { label: 'Dashboard', icon: IconServer, path: '/tropos' },
  { label: 'Regions', icon: IconMap, path: '/tropos/regions' },
  { label: 'Racks', icon: IconLayoutGrid, path: '/tropos/racks' },
  { label: 'Devices', icon: IconDevices, path: '/tropos/devices' },
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
      <AppShell.Navbar p="md" style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
        <Box mb="lg">
          <Text fw={700} size="lg">IAM Admin</Text>
        </Box>
        <Box style={{ flex: 1 }}>
          {iamNavItems.map((item) => (
            <NavLink
              key={item.path}
              label={item.label}
              leftSection={<item.icon size={18} />}
              active={location.pathname === item.path}
              onClick={() => navigate(item.path)}
              mb={4}
            />
          ))}
          <Divider my="sm" label="Tropos" labelPosition="left" />
          {troposNavItems.map((item) => (
            <NavLink
              key={item.path}
              label={item.label}
              leftSection={<item.icon size={18} />}
              active={location.pathname === item.path || (item.path !== '/tropos' && location.pathname.startsWith(item.path))}
              onClick={() => navigate(item.path)}
              mb={4}
            />
          ))}
        </Box>
        <NavLink
          label="Logout"
          leftSection={<IconLogout size={18} />}
          onClick={handleLogout}
          color="red"
        />
      </AppShell.Navbar>
      <AppShell.Main>
        <Outlet />
      </AppShell.Main>
    </AppShell>
  )
}
