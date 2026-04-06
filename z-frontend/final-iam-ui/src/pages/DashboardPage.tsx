import { Box, Grid, Card, Text, Title, Group, ThemeIcon, Stack, Button, Skeleton, Table, Badge } from '@mantine/core'
import { IconUsers, IconUserCheck, IconBuilding, IconUserPlus, IconArrowRight, IconAlertCircle } from '@tabler/icons-react'
import { useNavigate } from 'react-router-dom'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, PieChart, Pie, Cell, ResponsiveContainer } from 'recharts'
import { useGetDashboardSummaryQuery } from '../services/iamApi'

function StatCard({ label, value, icon: Icon, color, loading }: { label: string; value: number | undefined; icon: React.FC<{ size: number }>; color: string; loading: boolean }) {
  return (
    <Card withBorder p="lg" radius="md">
      <Group justify="space-between" align="flex-start">
        <Box>
          <Text size="sm" c="dimmed" mb={4}>{label}</Text>
          {loading ? (
            <Skeleton height={32} width={60} />
          ) : (
            <Title order={2}>{value ?? 0}</Title>
          )}
        </Box>
        <ThemeIcon color={color} variant="light" size="xl" radius="md">
          <Icon size={22} />
        </ThemeIcon>
      </Group>
    </Card>
  )
}

function getActionLabel(action: string): string {
  const labels: Record<string, string> = {
    'auth.login': 'Login',
    'auth.login_failed': 'Login Failed',
    'auth.logout': 'Logout',
    'user.create': 'User Created',
    'user.update': 'User Updated',
    'user.delete': 'User Deleted',
    'user.reset_password': 'Password Reset',
    'department.create': 'Department Created',
    'department.update': 'Department Updated',
    'department.delete': 'Department Deleted',
  }
  return labels[action] || action
}

export default function DashboardPage() {
  const navigate = useNavigate()
  const { data: dashboard, isLoading } = useGetDashboardSummaryQuery()

  if (isLoading) {
    return <Box p="xl"><Skeleton height={400} /></Box>
  }

  if (!dashboard) {
    return <Box p="xl"><Text>Failed to load dashboard</Text></Box>
  }

  const loginChartData = [
    { name: 'Successful', value: dashboard.login_success_7d },
    { name: 'Failed', value: dashboard.failed_logins_7d },
  ]

  const COLORS = ['#51cf66', '#ff6b6b']

  return (
    <Box>
      <Box mb="xl">
        <Title order={2}>Dashboard</Title>
        <Text c="dimmed" size="sm">System overview and recent activity</Text>
      </Box>

      <Grid mb="xl">
        <Grid.Col span={{ base: 12, sm: 6, md: 3 }}>
          <StatCard
            label="Total Users"
            value={dashboard.stats.total_users}
            icon={IconUsers}
            color="blue"
            loading={false}
          />
        </Grid.Col>
        <Grid.Col span={{ base: 12, sm: 6, md: 3 }}>
          <StatCard
            label="Active Users"
            value={dashboard.stats.active_users}
            icon={IconUserCheck}
            color="green"
            loading={false}
          />
        </Grid.Col>
        <Grid.Col span={{ base: 12, sm: 6, md: 3 }}>
          <StatCard
            label="Inactive Users"
            value={dashboard.stats.inactive_users}
            icon={IconAlertCircle}
            color="yellow"
            loading={false}
          />
        </Grid.Col>
        <Grid.Col span={{ base: 12, sm: 6, md: 3 }}>
          <StatCard
            label="Total Departments"
            value={dashboard.stats.total_departments}
            icon={IconBuilding}
            color="violet"
            loading={false}
          />
        </Grid.Col>
      </Grid>

      <Grid mb="xl">
        <Grid.Col span={{ base: 12, md: 6 }}>
          <Card withBorder p="lg" radius="md">
            <Title order={4} mb="md">Login Activity (Last 7 Days)</Title>
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={loginChartData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${name}: ${value}`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {COLORS.map((color, index) => (
                    <Cell key={`cell-${index}`} fill={color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Card>
        </Grid.Col>

        <Grid.Col span={{ base: 12, md: 6 }}>
          <Card withBorder p="lg" radius="md">
            <Title order={4} mb="md">Recent Activity</Title>
            <Stack gap="xs">
              {dashboard.recent_activity.slice(0, 5).map((log) => (
                <Group key={log.id} justify="space-between" align="center">
                  <Box>
                    <Text size="sm" fw={500}>{log.actor_name || log.actor || 'System'}</Text>
                    <Text size="xs" c="dimmed">{getActionLabel(log.action)}</Text>
                  </Box>
                  <Badge
                    color={log.status === 'success' ? 'green' : 'red'}
                    variant="light"
                    size="sm"
                  >
                    {log.status}
                  </Badge>
                </Group>
              ))}
            </Stack>
          </Card>
        </Grid.Col>
      </Grid>

      <Grid mb="xl">
        <Grid.Col span={{ base: 12, md: 6 }}>
          <Card withBorder p="lg" radius="md">
            <Title order={4} mb="md">Users by Department</Title>
            {dashboard.users_by_department.length > 0 ? (
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={dashboard.users_by_department}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" angle={-45} textAnchor="end" height={80} />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="user_count" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <Text c="dimmed" size="sm">No department data</Text>
            )}
          </Card>
        </Grid.Col>

        <Grid.Col span={{ base: 12, md: 6 }}>
          <Card withBorder p="lg" radius="md">
            <Title order={4} mb="md">Top Active Users (7 Days)</Title>
            <Stack gap="xs">
              {dashboard.top_actors.map((actor, idx) => (
                <Group key={idx} justify="space-between">
                  <Box>
                    <Text size="sm" fw={500}>{actor.name}</Text>
                    <Text size="xs" c="dimmed">@{actor.username}</Text>
                  </Box>
                  <Badge color="blue" variant="light">{actor.event_count} events</Badge>
                </Group>
              ))}
            </Stack>
          </Card>
        </Grid.Col>
      </Grid>

      <Card withBorder p="lg" radius="md" mb="xl">
        <Title order={4} mb="md">Recent Admin Actions</Title>
        {dashboard.recent_admin_actions.length > 0 ? (
          <Box style={{ overflowX: 'auto' }}>
            <Table striped highlightOnHover>
              <Table.Thead>
                <Table.Tr>
                  <Table.Th>Actor</Table.Th>
                  <Table.Th>Action</Table.Th>
                  <Table.Th>Target</Table.Th>
                  <Table.Th>Status</Table.Th>
                  <Table.Th>Time</Table.Th>
                </Table.Tr>
              </Table.Thead>
              <Table.Tbody>
                {dashboard.recent_admin_actions.map((log) => (
                  <Table.Tr key={log.id}>
                    <Table.Td>
                      <Text size="sm">{log.actor_name || log.actor || 'System'}</Text>
                    </Table.Td>
                    <Table.Td>
                      <Text size="sm">{getActionLabel(log.action)}</Text>
                    </Table.Td>
                    <Table.Td>
                      <Badge size="sm" variant="light">{log.target_type}</Badge>
                    </Table.Td>
                    <Table.Td>
                      <Badge
                        color={log.status === 'success' ? 'green' : 'red'}
                        variant="light"
                        size="sm"
                      >
                        {log.status}
                      </Badge>
                    </Table.Td>
                    <Table.Td>
                      <Text size="xs" c="dimmed">
                        {new Date(log.timestamp).toLocaleDateString()} {new Date(log.timestamp).toLocaleTimeString()}
                      </Text>
                    </Table.Td>
                  </Table.Tr>
                ))}
              </Table.Tbody>
            </Table>
          </Box>
        ) : (
          <Text c="dimmed" size="sm">No admin actions</Text>
        )}
      </Card>

      <Group>
        <Button leftSection={<IconUserPlus size={16} />} onClick={() => navigate('/users')}>
          Manage Users
        </Button>
        <Button variant="default" leftSection={<IconArrowRight size={16} />} onClick={() => navigate('/departments')}>
          Manage Departments
        </Button>
      </Group>
    </Box>
  )
}
