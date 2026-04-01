import { useState } from 'react'
import { Table, TextInput, Button, Badge, Group, Title, Paper, Text, Center, Loader } from '@mantine/core'
import { useListRegionsQuery } from '../../../services/inventoryApi'

export default function RegionsPage() {
  const [search, setSearch] = useState('')
  const [searchInput, setSearchInput] = useState('')

  const { data, isLoading, isError } = useListRegionsQuery({ search })

  const regions = data ?? []
  const filtered = search
    ? regions.filter((r) => r.name.toLowerCase().includes(search.toLowerCase()))
    : regions

  const handleSearch = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setSearch(searchInput)
  }

  return (
    <>
      <Group justify="space-between" mb="md">
        <Title order={3}>Regions</Title>
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
        {isError && <Center p="xl"><Text c="red" size="sm">Failed to load regions.</Text></Center>}
        {data && (
          <Table striped highlightOnHover>
            <Table.Thead>
              <Table.Tr>
                <Table.Th>ID</Table.Th>
                <Table.Th>Name</Table.Th>
                <Table.Th>Created</Table.Th>
              </Table.Tr>
            </Table.Thead>
            <Table.Tbody>
              {filtered.length === 0 ? (
                <Table.Tr>
                  <Table.Td colSpan={3}>
                    <Center p="md"><Text c="dimmed" size="sm">No regions found.</Text></Center>
                  </Table.Td>
                </Table.Tr>
              ) : (
                filtered.map((region) => (
                  <Table.Tr key={region.id}>
                    <Table.Td><Text size="sm" c="dimmed">{region.id}</Text></Table.Td>
                    <Table.Td><Text size="sm" fw={500}>{region.name}</Text></Table.Td>
                    <Table.Td><Text size="sm" c="dimmed">{new Date(region.created_at).toLocaleDateString()}</Text></Table.Td>
                  </Table.Tr>
                ))
              )}
            </Table.Tbody>
          </Table>
        )}
      </Paper>
    </>
  )
}
