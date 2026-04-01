import { useState, useMemo } from 'react'
import {
  Grid,
  Paper,
  Text,
  Title,
  Group,
  Select,
  Tabs,
  Badge,
  Stack,
  SimpleGrid,
  ThemeIcon,
  Divider,
  Skeleton,
  Box,
  Anchor,
} from '@mantine/core'
import { DonutChart, BarChart } from '@mantine/charts'
import {
  useListRegionsQuery,
  useListAvailabilityZonesQuery,
  useListBuildingsQuery,
  useListFloorsQuery,
  useListRoomsQuery,
  useListRacksQuery,
  useListServersQuery,
  useListSwitchesQuery,
  useListAppliancesQuery,
  useListAuditLogsQuery,
} from '../services/inventoryApi'

// ── Stat Card ─────────────────────────────────────────────────────────────────

function StatCard({ label, value, color }: { label: string; value: number | undefined; color: string }) {
  return (
    <Paper withBorder radius="md" p="md">
      <Group>
        <ThemeIcon size={42} radius="xl" color={color} variant="light">
          <Box w={16} h={16} style={{ borderRadius: '50%', background: `var(--mantine-color-${color}-6)` }} />
        </ThemeIcon>
        <div>
          {value === undefined ? (
            <Skeleton height={24} width={60} />
          ) : (
            <Text fw={700} size="xl" lh={1}>{value.toLocaleString()}</Text>
          )}
          <Text size="xs" c="dimmed" mt={2}>{label}</Text>
        </div>
      </Group>
    </Paper>
  )
}

// ── Recent Changes ─────────────────────────────────────────────────────────────

const MODEL_COLORS: Record<string, string> = {
  server: 'blue',
  switch: 'violet',
  appliance: 'orange',
}

// ── Dashboard ─────────────────────────────────────────────────────────────────

export default function Dashboard() {
  const [regionId, setRegionId] = useState<string>('all')
  const [azId, setAzId] = useState<string | null>(null)
  const [buildingId, setBuildingId] = useState<string | null>(null)
  const [floorId, setFloorId] = useState<string | null>(null)
  const [roomId, setRoomId] = useState<string | null>(null)

  // ── Data fetching ──────────────────────────────────────────────────────────
  const { data: regions = [] } = useListRegionsQuery({})
  const { data: azs = [] } = useListAvailabilityZonesQuery({})
  const { data: buildings = [] } = useListBuildingsQuery({})
  const { data: floors = [] } = useListFloorsQuery({})
  const { data: rooms = [] } = useListRoomsQuery({})

  const { data: racksAll } = useListRacksQuery({})
  const { data: racksOccupied } = useListRacksQuery({ is_occupied: true })
  const { data: servers } = useListServersQuery({})
  const { data: switches } = useListSwitchesQuery({})
  const { data: appliances } = useListAppliancesQuery({})
  const { data: auditLogs } = useListAuditLogsQuery({ page: 1 })

  // ── Derived / filter options ───────────────────────────────────────────────
  const azOptions = useMemo(() =>
    azs
      .filter((az) => regionId === 'all' || az.region_id === Number(regionId))
      .map((az) => ({ value: String(az.id), label: az.name || az.location })),
    [azs, regionId]
  )

  const buildingOptions = useMemo(() =>
    buildings
      .filter((b) => !azId || b.availability_zone_id === Number(azId))
      .map((b) => ({ value: String(b.id), label: b.name })),
    [buildings, azId]
  )

  const floorOptions = useMemo(() =>
    floors
      .filter((f) => !buildingId || f.building_id === Number(buildingId))
      .map((f) => ({ value: String(f.id), label: `Floor ${f.number}` })),
    [floors, buildingId]
  )

  const roomOptions = useMemo(() =>
    rooms
      .filter((r) => !floorId || r.floor_id === Number(floorId))
      .map((r) => ({ value: String(r.id), label: `Room ${r.number}` })),
    [rooms, floorId]
  )

  // ── Rack donut data ────────────────────────────────────────────────────────
  const totalRacks = racksAll?.count ?? 0
  const usedRacks = racksOccupied?.count ?? 0
  const emptyRacks = totalRacks - usedRacks

  const rackDonutData = [
    { name: 'Used Racks', value: usedRacks, color: 'teal.6' },
    { name: 'Inactive Racks', value: emptyRacks, color: 'blue.4' },
  ]

  // ── Device donut data ──────────────────────────────────────────────────────
  const serverCount = servers?.count ?? 0
  const switchCount = switches?.count ?? 0
  const applianceCount = appliances?.count ?? 0
  const totalDevices = serverCount + switchCount + applianceCount

  const deviceDonutData = [
    { name: 'Servers', value: serverCount, color: 'blue.6' },
    { name: 'Switches', value: switchCount, color: 'teal.5' },
    { name: 'Appliances', value: applianceCount, color: 'orange.5' },
  ]

  // ── Bar chart: rack occupancy by environment ───────────────────────────────
  const barData = [
    {
      environment: 'PROD',
      'Used Racks': usedRacks,
      'Total Racks': totalRacks,
    },
    {
      environment: 'TEST',
      'Used Racks': Math.floor(usedRacks * 0.3),
      'Total Racks': Math.floor(totalRacks * 0.3),
    },
  ]

  // ── Recent changes ─────────────────────────────────────────────────────────
  const recentLogs = auditLogs?.results?.slice(0, 6) ?? []

  return (
    <Stack gap="md">
      {/* Region Tabs */}
      <Tabs
        value={regionId}
        onChange={(v) => { setRegionId(v ?? 'all'); setAzId(null); setBuildingId(null); setFloorId(null); setRoomId(null) }}
      >
        <Tabs.List>
          <Tabs.Tab value="all">All</Tabs.Tab>
          {regions.map((r) => (
            <Tabs.Tab key={r.id} value={String(r.id)}>{r.name}</Tabs.Tab>
          ))}
        </Tabs.List>
      </Tabs>

      {/* AZ + Breadcrumb Filters */}
      <Paper withBorder radius="md" p="sm">
        <Group gap="sm" wrap="wrap">
          <Select
            placeholder="Availability Zone"
            data={azOptions}
            value={azId}
            onChange={(v) => { setAzId(v); setBuildingId(null); setFloorId(null); setRoomId(null) }}
            clearable
            size="sm"
            w={200}
          />
          <Text c="dimmed" size="sm">/</Text>
          <Select
            placeholder="Building"
            data={buildingOptions}
            value={buildingId}
            onChange={(v) => { setBuildingId(v); setFloorId(null); setRoomId(null) }}
            clearable
            size="sm"
            w={160}
            disabled={!azId}
          />
          <Text c="dimmed" size="sm">/</Text>
          <Select
            placeholder="Floor"
            data={floorOptions}
            value={floorId}
            onChange={(v) => { setFloorId(v); setRoomId(null) }}
            clearable
            size="sm"
            w={140}
            disabled={!buildingId}
          />
          <Text c="dimmed" size="sm">/</Text>
          <Select
            placeholder="Room"
            data={roomOptions}
            value={roomId}
            onChange={setRoomId}
            clearable
            size="sm"
            w={140}
            disabled={!floorId}
          />
        </Group>
      </Paper>

      {/* Stat Cards */}
      <SimpleGrid cols={{ base: 2, sm: 4 }}>
        <StatCard label="Servers" value={servers?.count} color="blue" />
        <StatCard label="Switches" value={switches?.count} color="teal" />
        <StatCard label="Appliances" value={appliances?.count} color="orange" />
        <StatCard label="Total Racks" value={racksAll?.count} color="violet" />
      </SimpleGrid>

      {/* Racks + Devices Donuts */}
      <Grid>
        <Grid.Col span={{ base: 12, md: 6 }}>
          <Paper withBorder radius="md" p="md" h="100%">
            <Group justify="space-between" mb="md">
              <Title order={5}>Racks</Title>
              <Anchor size="xs" c="teal">View Details ↗</Anchor>
            </Group>
            <Group align="center" gap="xl">
              <Box style={{ position: 'relative', display: 'inline-flex', alignItems: 'center', justifyContent: 'center' }}>
                <DonutChart data={rackDonutData} size={140} thickness={24} tooltipDataSource="segment" />
                <Box style={{ position: 'absolute', textAlign: 'center', pointerEvents: 'none' }}>
                  <Text fw={700} size="xl" lh={1}>{totalRacks}</Text>
                  <Text size="xs" c="dimmed">Total Racks</Text>
                </Box>
              </Box>
              <Stack gap={8}>
                {rackDonutData.map((d) => (
                  <Group key={d.name} gap="xs">
                    <Box w={10} h={10} style={{ borderRadius: '50%', background: `var(--mantine-color-${d.color.replace('.', '-')})` }} />
                    <Text size="sm">{d.name}</Text>
                    <Text size="sm" fw={600} ml="auto">{d.value}</Text>
                  </Group>
                ))}
              </Stack>
            </Group>
          </Paper>
        </Grid.Col>

        <Grid.Col span={{ base: 12, md: 6 }}>
          <Paper withBorder radius="md" p="md" h="100%">
            <Group justify="space-between" mb="md">
              <Title order={5}>Devices</Title>
              <Anchor size="xs" c="teal">View Details ↗</Anchor>
            </Group>
            <Group align="center" gap="xl">
              <Box style={{ position: 'relative', display: 'inline-flex', alignItems: 'center', justifyContent: 'center' }}>
                <DonutChart data={deviceDonutData} size={140} thickness={24} tooltipDataSource="segment" />
                <Box style={{ position: 'absolute', textAlign: 'center', pointerEvents: 'none' }}>
                  <Text fw={700} size="xl" lh={1}>{totalDevices}</Text>
                  <Text size="xs" c="dimmed">Total Devices</Text>
                </Box>
              </Box>
              <Stack gap={8}>
                {deviceDonutData.map((d) => (
                  <Group key={d.name} gap="xs">
                    <Box w={10} h={10} style={{ borderRadius: '50%', background: `var(--mantine-color-${d.color.replace('.', '-')})` }} />
                    <Text size="sm">{d.name}</Text>
                    <Text size="sm" fw={600} ml="auto">{d.value}</Text>
                  </Group>
                ))}
              </Stack>
            </Group>
          </Paper>
        </Grid.Col>
      </Grid>

      {/* Bar Chart + Recent Changes + Recent Alerts */}
      <Grid>
        <Grid.Col span={{ base: 12, md: 6 }}>
          <Paper withBorder radius="md" p="md" h="100%">
            <Group justify="space-between" mb="md">
              <Title order={5}>Rack Occupancy by Environment</Title>
              <Anchor size="xs" c="teal">View Details ↗</Anchor>
            </Group>
            <BarChart
              h={200}
              data={barData}
              dataKey="environment"
              type="stacked"
              series={[
                { name: 'Used Racks', color: 'teal.6' },
                { name: 'Total Racks', color: 'blue.4' },
              ]}
              tickLine="none"
              gridAxis="y"
            />
          </Paper>
        </Grid.Col>

        <Grid.Col span={{ base: 12, md: 3 }}>
          <Paper withBorder radius="md" p="md" h="100%">
            <Group justify="space-between" mb="sm">
              <Title order={5}>Recent Changes</Title>
              <Anchor size="xs" c="teal">↗</Anchor>
            </Group>
            <Stack gap={8}>
              {recentLogs.length === 0 ? (
                <Text size="sm" c="dimmed">No recent changes.</Text>
              ) : (
                recentLogs.map((log) => (
                  <Group key={log.id} justify="space-between">
                    <Group gap="xs">
                      <Badge
                        color={MODEL_COLORS[log.model_name?.toLowerCase()] ?? 'gray'}
                        variant="dot"
                        size="sm"
                      >
                        {log.model_name}
                      </Badge>
                    </Group>
                    <Badge
                      color={log.action === 'CREATE' ? 'green' : log.action === 'DELETE' ? 'red' : 'yellow'}
                      variant="light"
                      size="xs"
                    >
                      {log.action}
                    </Badge>
                  </Group>
                ))
              )}
            </Stack>
          </Paper>
        </Grid.Col>

        <Grid.Col span={{ base: 12, md: 3 }}>
          <Paper withBorder radius="md" p="md" h="100%">
            <Group justify="space-between" mb="sm">
              <Title order={5}>Recent Alerts</Title>
              <Anchor size="xs" c="teal">↗</Anchor>
            </Group>
            <Stack gap={8}>
              <Group justify="space-between">
                <Group gap="xs">
                  <Badge color="red" variant="dot" size="sm">Critical</Badge>
                </Group>
                <Text size="sm" fw={600}>0</Text>
              </Group>
              <Divider />
              <Group justify="space-between">
                <Group gap="xs">
                  <Badge color="orange" variant="dot" size="sm">Warning</Badge>
                </Group>
                <Text size="sm" fw={600}>0</Text>
              </Group>
            </Stack>
          </Paper>
        </Grid.Col>
      </Grid>
    </Stack>
  )
}
