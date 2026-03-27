import { useState } from "react"
import { Title, Group, Select, TextInput, Badge, Text, Stack, Button, Modal, ActionIcon, Code, ScrollArea } from "@mantine/core"
import { IconEye } from "@tabler/icons-react"
import { DataTable } from "mantine-datatable"
import { useGetAuditLogsQuery, useGetMeQuery } from "../services/iamApi"
import type { AuditLog, AuditLogParams } from "../types"

const ACTION_LABELS: Record<string, string> = {
  "auth.login":            "Login",
  "auth.login_failed":     "Login Failed",
  "auth.logout":           "Logout",
  "auth.token_refresh":    "Token Refresh",
  "user.create":           "User Created",
  "user.update":           "User Updated",
  "user.delete":           "User Deleted",
  "user.reset_password":   "Password Reset",
  "user.change_password":  "Password Changed",
  "department.create":     "Department Created",
  "department.update":     "Department Updated",
  "department.delete":     "Department Deleted",
}

const ACTION_OPTIONS = [
  { value: "", label: "All Actions" },
  ...Object.entries(ACTION_LABELS).map(([value, label]) => ({ value, label })),
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

  const getTargetName = (log: AuditLog) =>
    log.detail?.name ?? log.detail?.username ?? log.detail?.target ?? null

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
            width: 160,
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
            width: 130,
            render: (log) => log.actor ?? <Text c="dimmed" size="sm">anonymous</Text>,
          },
          {
            accessor: "department",
            title: "Department",
            width: 130,
            render: (log) => log.department ?? "—",
          },
          {
            accessor: "action",
            title: "Action",
            width: 180,
            render: (log) => ACTION_LABELS[log.action] ?? log.action,
          },
          {
            accessor: "target",
            title: "Target",
            width: 150,
            render: (log) => {
              const name = getTargetName(log)
              return name
                ? <Text size="sm">{name}</Text>
                : <Text size="sm" c="dimmed">—</Text>
            },
          },
          {
            accessor: "status",
            title: "Status",
            width: 90,
            render: (log) => (
              <Badge color={log.status === "success" ? "green" : "red"} variant="light" size="sm">
                {log.status}
              </Badge>
            ),
          },
          {
            accessor: "ip_address",
            title: "IP Address",
            width: 120,
            render: (log) => log.ip_address ?? "—",
          },
          {
            accessor: "browser",
            title: "Browser",
            width: 150,
            render: (log) => log.detail?.browser ?? "—",
          },
          {
            accessor: "os",
            title: "OS / Device",
            width: 150,
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
            <Text fw={600} size="sm">{detailLog ? ACTION_LABELS[detailLog.action] ?? detailLog.action : ""}</Text>
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
