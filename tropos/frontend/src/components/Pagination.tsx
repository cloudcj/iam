import { Group, Pagination as MantinePagination, Text } from '@mantine/core'

interface Props {
  page: number
  numPages: number
  count: number
  perPage: number
  onPage: (page: number) => void
}

export default function Pagination({ page, numPages, count, perPage, onPage }: Props) {
  const from = (page - 1) * perPage + 1
  const to = Math.min(page * perPage, count)

  return (
    <Group justify="space-between" px="md" py="sm" style={{ borderTop: '1px solid var(--mantine-color-gray-2)' }}>
      <Text size="sm" c="dimmed">{from}–{to} of {count}</Text>
      <MantinePagination total={numPages} value={page} onChange={onPage} size="sm" />
    </Group>
  )
}
