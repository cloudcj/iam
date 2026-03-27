import { useState } from "react"
import { Title, Group, Select, TextInput, Badge, Text, Stack, Button, Modal, ActionIcon, Code, ScrollArea } from "@mantine/core"
import { IconEye } from "@tabler/icons-react"
import { DataTable } from "mantine-datatable"
import { useGetAuditLogsQuery, useGetMeQuery } from "../services/iamApi"
import type { AuditLog, AuditLogParams } from "../types"

const ACTION_OPTIONS = [
  { value: "", label: "All Actions" },
  { value: "auth.login", label: "Login" },
  { value: "auth.login_failed", label: "Login Failed" },
  { value: "auth.logout", label: "Logout" },
  { value: "auth.token_refresh", label: "Token Refresh" },
  { value: "user.create", label: "User Created" },
  { value: "user.update", label: "User Updated" },
  { value: "user.delete", label: "User Deleted" },
  { value: "user.reset_password", label: "Password Reset" },
  { value: "user.change_password", label: "Password Changed" },
  { value: "dept.create", label: "Department Created" },
  { value: "dept.update", label: "Department Updated" },
  { value: "dept.delete", label: "Department Deleted" },
]

const PAGE_SIZE = 20

export default function AuditLogPage() {
  const { data: me } = useGetMeQuery()
  const [page, setPage] = useState(1)
  const [filters, setFilters] = useState<AuditLogParams>({})
  const [detailLog, setDetailLog] = useState<AuditLog | null>(null)

  const canView = me?.is_superuser || me?.permissions.includes("iam.audit.read")

  const params: AuditLogParams = {
    ...filters,
    limit: PAGE_SIZE,
    offset: (page - 1) * PAGE_SIZE,
  }

  const { data, isLoading } = useGetAuditLogsQuery(params, { skip: !canView })

  const setFilter = (key: keyof AuditLogParams, value: string) => {
    setPage(1)
    setFilters((prev) => ({ ...prev, [key]: value || undefined }))
  }

  const clearFilters = () => {
    setPage(1)
    setFilters({})
  }

  if (!canView) {
    return <Text c="red">You do not have permission to view audit logs.</Text>
  }

  return (
    <>
      <Group justify="space-between" mb="md">
        <Title order={3}>Audit Logs</Title>
        <Button variant="subtle" size="xs" onClick={clearFilters}>Clear Filters</Button>
      </Group>

      <Stack gap="sm" mb="md">
        <Group>
          <Select
            placeholder="All Actions"
            data={ACTION_OPTIONS}
            value={filters.action ?? ""}
            onChange={(v) => setFilter("action", v ?? "")}
            clearable
            style={{ width: 200 }}
          />
          <Select
            placeholder="All Statuses"
            data={[
              { value: "", label: "All Statuses" },
              { value: "success", label: "Success" },
              { value: "failure", label: "Failure" },
            ]}
            value={filters.status ?? ""}
            onChange={(v) => setFilter("status", v ?? "")}
            clearable
            style={{ width: 160 }}
          />
          <TextInput
            placeholder="From (YYYY-MM-DD)"
            value={filters.date_from ?? ""}
            onChange={(e) => setFilter("date_from", e.currentTarget.value)}
            style={{ width: 180 }}
          />
          <TextInput
            placeholder="To (YYYY-MM-DD)"
            value={filters.date_to ?? ""}
            onChange={(e) => setFilter("date_to", e.currentTarget.value)}
            style={{ width: 180 }}
          />
        </Group>
      </Stack>

      <DataTable
        withTableBorder
        withColumnBorders
        striped
        highlightOnHover
        fetching={isLoading}
        minHeight={150}
        noRecordsText="No audit logs found"
        records={data?.results ?? []}
        totalRecords={data?.count ?? 0}
        recordsPerPage={PAGE_SIZE}
        page={page}
        onPageChange={setPage}
        idAccessor="id"
        columns={[
          {
            accessor: "timestamp",
            title: "Timestamp",
            width: 180,
            render: (log) => {
              const d = new Date(log.timestamp)
              return (
                <Stack gap={0}>
                  <Text size="sm">{d.toLocaleDateString()}</Text>
                  <Text size="xs" c="dimmed">{d.toLocaleTimeString()}</Text>
                </Stack>
              )
            },
          },
          {
            accessor: "actor",
            title: "Actor",
            width: 140,
            render: (log) => log.actor ?? <Text c="dimmed" size="sm">anonymous</Text>,
          },
          {
            accessor: "department",
            title: "Department",
            width: 140,
            render: (log) => log.department ?? "—",
          },
          {
            accessor: "action",
            title: "Action",
            width: 180,
            render: (log) => (
              <Text size="sm" ff="monospace">{log.action}</Text>
            ),
          },
          {
            accessor: "status",
            title: "Status",
            width: 100,
            render: (log) => (
              <Badge color={log.status === "success" ? "green" : "red"} variant="light" size="sm">
                {log.status}
              </Badge>
            ),
          },
          {
            accessor: "target_type",
            title: "Target",
            width: 100,
            render: (log) => log.target_type || "—",
          },
          {
            accessor: "ip_address",
            title: "IP Address",
            width: 130,
            render: (log) => log.ip_address ?? "—",
          },
          {
            accessor: "browser",
            title: "Browser",
            width: 160,
            render: (log) => log.detail?.browser ?? "—",
            },
            {
            accessor: "os",
            title: "OS / Device",
            width: 160,
            render: (log) =>
                log.detail?.os
                ? `${log.detail.os} · ${log.detail.device}`
                : "—",
            },
          {
            accessor: "detail",
            title: "Details",
            width: 70,
            textAlign: "center",
            render: (log) =>
              Object.keys(log.detail).length > 0 ? (
                <ActionIcon
                  size="sm"
                  variant="subtle"
                  color="blue"
                  onClick={() => setDetailLog(log)}
                >
                  <IconEye size={16} />
                </ActionIcon>
              ) : "—",
          },
        ]}
      />
      <Modal
        opened={!!detailLog}
        onClose={() => setDetailLog(null)}
        title={
          <Stack gap={2}>
            <Text fw={600} size="sm">{detailLog?.action}</Text>
            <Text size="xs" c="dimmed">{detailLog ? new Date(detailLog.timestamp).toLocaleString() : ""}</Text>
          </Stack>
        }
      >
        <ScrollArea>
          <Code block>{JSON.stringify({
            name: detailLog?.actor_name ?? "anonymous",
            department: detailLog?.department ?? null,
            ...detailLog?.detail,
          }, null, 2)}</Code>
        </ScrollArea>
      </Modal>
    </>
  )
}
