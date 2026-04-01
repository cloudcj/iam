import { useState } from 'react'
import { Table, TextInput, Button, Badge, Group, Title, Paper, Text, Center, Loader } from '@mantine/core'
import { useListSwitchesQuery } from '../../services/inventoryApi'
import Pagination from '../../components/Pagination'

const statusColor: Record<string, string> = {
  ACTIVE: 'green',
  INACTIVE: 'gray',
  DECOMMISSIONED: 'red',
}

export default function SwitchesPage() {
  const [page, setPage] = useState(1)
  const [search, setSearch] = useState('')
  const [searchInput, setSearchInput] = useState('')

  const { data, isLoading, isError } = useListSwitchesQuery({ page, search })

  const handleSearch = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setPage(1)
    setSearch(searchInput)
  }

  return (
    <>
      <Group justify="space-between" mb="md">
        <Title order={3}>Switches</Title>
        <form onSubmit={handleSearch}>
          <Group gap="xs">
            <TextInput
              placeholder="Search…"
              value={searchInput}
              onChange={(e) => setSearchInput(e.currentTarget.value)}
              size="sm"
            />
            <Button type="submit" size="sm">Search</Button>
          </Group>
        </form>
      </Group>

      <Paper withBorder radius="md" style={{ overflow: 'hidden' }}>
        {isLoading && <Center p="xl"><Loader size="sm" /></Center>}
        {isError && <Center p="xl"><Text c="red" size="sm">Failed to load switches.</Text></Center>}
        {data && (
          <>
            <Table striped highlightOnHover>
              <Table.Thead>
                <Table.Tr>
                  <Table.Th>Name</Table.Th>
                  <Table.Th>Status</Table.Th>
                  <Table.Th>Model</Table.Th>
                  <Table.Th>Serial No.</Table.Th>
                  <Table.Th>IP Address</Table.Th>
                  <Table.Th>Interfaces</Table.Th>
                </Table.Tr>
              </Table.Thead>
              <Table.Tbody>
                {data.results.length === 0 ? (
                  <Table.Tr>
                    <Table.Td colSpan={6}>
                      <Center p="md"><Text c="dimmed" size="sm">No switches found.</Text></Center>
                    </Table.Td>
                  </Table.Tr>
                ) : (
                  data.results.map((sw, i) => (
                    <Table.Tr key={sw.device?.id ?? i}>
                      <Table.Td><Text size="sm" fw={500}>{sw.device?.name}</Text></Table.Td>
                      <Table.Td>
                        <Badge color={statusColor[sw.device?.status] ?? 'gray'} variant="light" size="sm">
                          {sw.device?.status}
                        </Badge>
                      </Table.Td>
                      <Table.Td><Text size="sm">{sw.device?.model}</Text></Table.Td>
                      <Table.Td><Text size="sm" ff="monospace" c="dimmed">{sw.device?.serial_number}</Text></Table.Td>
                      <Table.Td><Text size="sm" ff="monospace" c="dimmed">{sw.device?.ipv4_address ?? '—'}</Text></Table.Td>
                      <Table.Td><Text size="sm">{sw.device?.interface_count ?? '—'}</Text></Table.Td>
                    </Table.Tr>
                  ))
                )}
              </Table.Tbody>
            </Table>
            <Pagination
              page={data.page}
              numPages={data.num_pages}
              count={data.count}
              perPage={data.per_page}
              onPage={setPage}
            />
          </>
        )}
      </Paper>
    </>
  )
}
