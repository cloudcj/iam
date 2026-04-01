import { useState } from "react"
import { Title, Group, Select, TextInput, Badge, Text, Stack, Button, Modal, ActionIcon, Code, ScrollArea, Tabs } from "@mantine/core"
import { IconEye } from "@tabler/icons-react"
import { DataTable } from "mantine-datatable"
import { useGetAuditLogsQuery, useGetMeQuery } from "../services/iamApi"
import type { AuditLog, AuditLogParams } from "../types"

const AUTH_ACTION_LABELS: Record<string, string> = {
  "auth.login":         "Login",
  "auth.login_failed":  "Login Failed",
  "auth.logout":        "Logout",
  "auth.token_refresh": "Token Refresh",
}

const ACTIVITY_ACTION_LABELS: Record<string, string> = {
  "user.create":           "User Created",
  "user.update":           "User Updated",
  "user.delete":           "User Deleted",
  "user.reset_password":   "Password Reset",
  "user.change_password":  "Password Changed",
  "department.create":     "Department Created",
  "department.update":     "Department Updated",
  "department.delete":     "Department Deleted",
}

const ALL_ACTION_LABELS = { ...AUTH_ACTION_LABELS, ...ACTIVITY_ACTION_LABELS }

const AUTH_ACTION_OPTIONS = [
  { value: "", label: "All" },
  ...Object.entries(AUTH_ACTION_LABELS).map(([value, label]) => ({ value, label })),
]

const ACTIVITY_ACTION_OPTIONS = [
  { value: "", label: "All" },
  ...Object.entries(ACTIVITY_ACTION_LABELS).map(([value, label]) => ({ value, label })),
]

const PAGE_SIZE = 20

function LogTable({
  actionOptions,
  actionCategory,
  canView,
}: {
  actionOptions: { value: string; label: string }[]
  actionCategory: "auth" | "activity"
  canView: boolean
}) {
  const [page, setPage] = useState(1)
  const [filters, setFilters] = useState<Omit<AuditLogParams, "action_category" | "limit" | "offset">>({})
  const [detailLog, setDetailLog] = useState<AuditLog | null>(null)

  const params: AuditLogParams = {
    ...filters,
    action_category: actionCategory,
    limit: PAGE_SIZE,
    offset: (page - 1) * PAGE_SIZE,
  }

  const { data, isLoading } = useGetAuditLogsQuery(params, { skip: !canView })

  const setFilter = (key: keyof typeof filters, value: string) => {
    setPage(1)
    setFilters((prev) => ({ ...prev, [key]: value || undefined }))
  }

  const clearFilters = () => {
    setPage(1)
    setFilters({})
  }

  const getTargetName = (log: AuditLog) =>
    log.detail?.name ?? log.detail?.username ?? log.detail?.target ?? null

  return (
    <>
      <Stack gap="sm" mb="md">
        <Group>
          <Select
            placeholder="All Actions"
            data={actionOptions}
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
          <Button variant="subtle" size="xs" onClick={clearFilters}>Clear</Button>
        </Group>
      </Stack>

      <DataTable
        withTableBorder
        withColumnBorders
        striped
        highlightOnHover
        fetching={isLoading}
        minHeight={150}
        noRecordsText="No logs found"
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
            render: (log) => ALL_ACTION_LABELS[log.action] ?? log.action,
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
            <Text fw={600} size="sm">{detailLog ? ALL_ACTION_LABELS[detailLog.action] ?? detailLog.action : ""}</Text>
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

export default function AuditLogPage() {
  const { data: me } = useGetMeQuery()
  const canView = me?.is_superuser || me?.permissions.includes("iam.audit.read")

  if (!canView) {
    return <Text c="red">You do not have permission to view audit logs.</Text>
  }

  return (
    <>
      <Group justify="space-between" mb="md">
        <Title order={3}>Audit Logs</Title>
      </Group>

      <Tabs defaultValue="auth">
        <Tabs.List mb="md">
          <Tabs.Tab value="auth">Login Activity</Tabs.Tab>
          <Tabs.Tab value="activity">Activity Log</Tabs.Tab>
        </Tabs.List>

        <Tabs.Panel value="auth">
          <LogTable
            actionOptions={AUTH_ACTION_OPTIONS}
            actionCategory="auth"
            canView={!!canView}
          />
        </Tabs.Panel>

        <Tabs.Panel value="activity">
          <LogTable
            actionOptions={ACTIVITY_ACTION_OPTIONS}
            actionCategory="activity"
            canView={!!canView}
          />
        </Tabs.Panel>
      </Tabs>
    </>
  )
}
