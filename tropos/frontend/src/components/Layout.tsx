import { NavLink, Outlet, useLocation } from 'react-router-dom'
import { AppShell, NavLink as MantineNavLink, Text, Stack, ScrollArea, Box } from '@mantine/core'

const navGroups = [
  {
    label: null,
    items: [
      { to: '/dashboard', label: 'Dashboard' },
    ],
  },
  {
    label: 'Infrastructure',
    items: [
      { to: '/infrastructure/regions', label: 'Regions' },
      { to: '/infrastructure/racks', label: 'Racks' },
    ],
  },
  {
    label: 'Assets',
    items: [
      { to: '/assets/devices', label: 'All Devices' },
      { to: '/assets/servers', label: 'Servers' },
      { to: '/assets/switches', label: 'Switches' },
      { to: '/assets/appliances', label: 'Appliances' },
    ],
  },
  {
    label: 'Users',
    items: [{ to: '/users', label: 'User Accounts' }],
  },
]

export default function Layout() {
  const location = useLocation()

  return (
    <AppShell navbar={{ width: 220, breakpoint: 'sm' }} padding="md">
      <AppShell.Navbar p="sm">
        <AppShell.Section>
          <Box px="xs" py="sm">
            <Text fw={700} size="lg">Inventory</Text>
          </Box>
        </AppShell.Section>

        <AppShell.Section grow component={ScrollArea}>
          <Stack gap={0}>
            {navGroups.map((group, i) => (
              <Box key={i} mb="sm">
                {group.label && (
                  <Text size="xs" fw={600} c="dimmed" tt="uppercase" px="xs" mb={4}>
                    {group.label}
                  </Text>
                )}
                {group.items.map((item) => (
                  <MantineNavLink
                    key={item.to}
                    component={NavLink}
                    to={item.to}
                    label={item.label}
                    active={location.pathname === item.to}
                    style={{ borderRadius: 6 }}
                  />
                ))}
              </Box>
            ))}
          </Stack>
        </AppShell.Section>
      </AppShell.Navbar>

      <AppShell.Main>
        <Outlet />
      </AppShell.Main>
    </AppShell>
  )
}
