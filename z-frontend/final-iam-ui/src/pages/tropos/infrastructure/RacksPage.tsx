import { useState } from 'react'
import { Table, TextInput, Button, Badge, Group, Title, Paper, Text, Center, Loader } from '@mantine/core'
import { useListRacksQuery } from '../../../services/inventoryApi'
import Pagination from '../../../components/Pagination'

export default function RacksPage() {
  const [page, setPage] = useState(1)
  const [search, setSearch] = useState('')
  const [searchInput, setSearchInput] = useState('')

  const { data, isLoading, isError } = useListRacksQuery({ page, search })

  const handleSearch = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setPage(1)
    setSearch(searchInput)
  }

  return (
    <>
      <Group justify="space-between" mb="md">
        <Title order={3}>Racks</Title>
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
        {isError && <Center p="xl"><Text c="red" size="sm">Failed to load racks.</Text></Center>}
        {data && (
          <>
            <Table striped highlightOnHover>
              <Table.Thead>
                <Table.Tr>
                  <Table.Th>Number</Table.Th>
                  <Table.Th>Environment</Table.Th>
                  <Table.Th>RU Count</Table.Th>
                  <Table.Th>Occupied</Table.Th>
                </Table.Tr>
              </Table.Thead>
              <Table.Tbody>
                {data.results.length === 0 ? (
                  <Table.Tr>
                    <Table.Td colSpan={4}>
                      <Center p="md"><Text c="dimmed" size="sm">No racks found.</Text></Center>
                    </Table.Td>
                  </Table.Tr>
                ) : (
                  data.results.map((rack) => (
                    <Table.Tr key={rack.id}>
                      <Table.Td><Text size="sm" fw={500}>{rack.number}</Text></Table.Td>
                      <Table.Td>
                        <Badge color={rack.environment === 'PROD' ? 'blue' : 'yellow'} variant="light" size="sm">
                          {rack.environment}
                        </Badge>
                      </Table.Td>
                      <Table.Td><Text size="sm">{rack.ru_count}U</Text></Table.Td>
                      <Table.Td>
                        <Badge color={rack.is_occupied ? 'green' : 'gray'} variant="dot" size="sm">
                          {rack.is_occupied ? 'Occupied' : 'Empty'}
                        </Badge>
                      </Table.Td>
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
