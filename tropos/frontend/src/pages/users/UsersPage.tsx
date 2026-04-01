import { useState } from 'react'
import { Table, TextInput, Button, Badge, Group, Title, Paper, Text, Center, Loader } from '@mantine/core'
import { useListUsersQuery } from '../../services/inventoryApi'
import Pagination from '../../components/Pagination'

export default function UsersPage() {
  const [page, setPage] = useState(1)
  const [search, setSearch] = useState('')
  const [searchInput, setSearchInput] = useState('')

  const { data, isLoading, isError } = useListUsersQuery({ page, search })

  const handleSearch = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setPage(1)
    setSearch(searchInput)
  }

  return (
    <>
      <Group justify="space-between" mb="md">
        <Title order={3}>User Accounts</Title>
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
        {isError && <Center p="xl"><Text c="red" size="sm">Failed to load users.</Text></Center>}
        {data && (
          <>
            <Table striped highlightOnHover>
              <Table.Thead>
                <Table.Tr>
                  <Table.Th>Username</Table.Th>
                  <Table.Th>Name</Table.Th>
                  <Table.Th>Email</Table.Th>
                  <Table.Th>Status</Table.Th>
                </Table.Tr>
              </Table.Thead>
              <Table.Tbody>
                {data.results.length === 0 ? (
                  <Table.Tr>
                    <Table.Td colSpan={4}>
                      <Center p="md"><Text c="dimmed" size="sm">No users found.</Text></Center>
                    </Table.Td>
                  </Table.Tr>
                ) : (
                  data.results.map((user) => (
                    <Table.Tr key={user.id}>
                      <Table.Td><Text size="sm" fw={500}>{user.username}</Text></Table.Td>
                      <Table.Td>
                        <Text size="sm">{[user.first_name, user.last_name].filter(Boolean).join(' ') || '—'}</Text>
                      </Table.Td>
                      <Table.Td><Text size="sm" c="dimmed">{user.email || '—'}</Text></Table.Td>
                      <Table.Td>
                        <Badge color={user.is_active ? 'green' : 'gray'} variant="light" size="sm">
                          {user.is_active ? 'Active' : 'Inactive'}
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
