import { Box, Grid, Card, Text, Title, Group, ThemeIcon, Stack, Button, Skeleton } from '@mantine/core'
import { IconUsers, IconUserCheck, IconBuilding, IconUserPlus, IconArrowRight } from '@tabler/icons-react'
import { useNavigate } from 'react-router-dom'
import { useGetUsersQuery, useGetDepartmentsQuery, useGetMeQuery } from '../services/iamApi'

interface StatCardProps {
  label: string
  value: number | undefined
  icon: React.FC<{ size: number }>
  color: string
  loading: boolean
}

function StatCard({ label, value, icon: Icon, color, loading }: StatCardProps) {
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

export default function DashboardPage() {
  const navigate = useNavigate()
  const { data: me } = useGetMeQuery()
  const { data: users, isLoading: usersLoading } = useGetUsersQuery()
  const { data: departments, isLoading: deptsLoading } = useGetDepartmentsQuery()

  const totalUsers = users?.length
  const activeUsers = users?.filter((u) => u.is_active).length
  const totalDepartments = departments?.length

  return (
    <Box>
      <Box mb="xl">
        <Title order={2}>Welcome back, {me?.first_name || me?.username}</Title>
        <Text c="dimmed" size="sm">Here's an overview of your IAM system.</Text>
      </Box>

      <Grid mb="xl">
        <Grid.Col span={{ base: 12, sm: 4 }}>
          <StatCard
            label="Total Users"
            value={totalUsers}
            icon={IconUsers}
            color="blue"
            loading={usersLoading}
          />
        </Grid.Col>
        <Grid.Col span={{ base: 12, sm: 4 }}>
          <StatCard
            label="Active Users"
            value={activeUsers}
            icon={IconUserCheck}
            color="green"
            loading={usersLoading}
          />
        </Grid.Col>
        <Grid.Col span={{ base: 12, sm: 4 }}>
          <StatCard
            label="Total Departments"
            value={totalDepartments}
            icon={IconBuilding}
            color="violet"
            loading={deptsLoading}
          />
        </Grid.Col>
      </Grid>

      <Title order={4} mb="sm">Quick Actions</Title>
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
