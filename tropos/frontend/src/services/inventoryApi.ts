import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'

// ── Shared ────────────────────────────────────────────────────────────────────

export interface PaginatedResponse<T> {
  page: number
  per_page: number
  num_pages: number
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export interface ListParams {
  page?: number
  search?: string
  [key: string]: string | number | boolean | undefined
}

// ── Infrastructure ─────────────────────────────────────────────────────────────

export interface Region {
  id: number
  name: string
  created_at: string
  updated_at: string
}

export interface AvailabilityZone {
  id: number
  name: string
  location: string
  region_id: number
  created_at: string
  updated_at: string
}

export interface Building {
  id: number
  name: string
  availability_zone_id: number
  created_at: string
  updated_at: string
}

export interface Floor {
  id: number
  number: string
  building_id: number
  created_at: string
  updated_at: string
}

export interface Room {
  id: number
  number: string
  floor_id: number
  created_at: string
  updated_at: string
}

export interface Rack {
  id: number
  number: string
  environment: 'TEST' | 'PROD'
  ru_count: number
  weight: number | null
  is_occupied: boolean
  pod: number
  network_area: number | null
  created_at: string
  updated_at: string
}

// ── Assets ─────────────────────────────────────────────────────────────────────

export interface Device {
  id: number
  name: string
  type: 'SERVER' | 'SWITCH' | 'APPLIANCE'
  status: 'ACTIVE' | 'INACTIVE' | 'DECOMMISSIONED'
  model: string
  serial_number: string
  ipv4_address: string | null
  weight: number | null
  power: number | null
  interface_count: number | null
  description: string
  rack: number
  created_at: string
  updated_at: string
}

export interface Server {
  classification: string
  device: Device
}

export interface Switch {
  device: Device
}

export interface ApplianceType {
  id: number
  name: string
}

export interface Appliance {
  appliance_type: ApplianceType | null
  device: Device
  is_chassis: boolean
  has_components_units: boolean
}

// ── Users ──────────────────────────────────────────────────────────────────────

export interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
  is_active: boolean
  groups: number[]
  created_at: string
  updated_at: string
}

// ── Logs ───────────────────────────────────────────────────────────────────────

export interface AuditLog {
  id: number
  username: string
  model_name: string
  action: 'CREATE' | 'UPDATE' | 'DELETE'
  changes: Record<string, unknown>
  timestamp: string
}

// ── API ────────────────────────────────────────────────────────────────────────

const buildQuery = (params: ListParams) => {
  const query = new URLSearchParams()
  Object.entries(params).forEach(([k, v]) => {
    if (v !== undefined && v !== '') query.set(k, String(v))
  })
  return query.toString()
}

export const inventoryApi = createApi({
  reducerPath: 'inventoryApi',
  baseQuery: fetchBaseQuery({ baseUrl: '/api/inventory/' }),
  tagTypes: ['Region', 'AvailabilityZone', 'Building', 'Floor', 'Room', 'Rack', 'Device', 'Server', 'Switch', 'Appliance', 'User'],
  endpoints: (builder) => ({
    // ── Infrastructure (plain lists) ──
    listRegions: builder.query<Region[], ListParams>({
      query: (params = {}) => `regions/?${buildQuery(params)}`,
      providesTags: ['Region'],
    }),
    listAvailabilityZones: builder.query<AvailabilityZone[], ListParams>({
      query: (params = {}) => `availability-zones/?${buildQuery(params)}`,
      providesTags: ['AvailabilityZone'],
    }),
    listBuildings: builder.query<Building[], ListParams>({
      query: (params = {}) => `buildings/?${buildQuery(params)}`,
      providesTags: ['Building'],
    }),
    listFloors: builder.query<Floor[], ListParams>({
      query: (params = {}) => `floors/?${buildQuery(params)}`,
      providesTags: ['Floor'],
    }),
    listRooms: builder.query<Room[], ListParams>({
      query: (params = {}) => `rooms/?${buildQuery(params)}`,
      providesTags: ['Room'],
    }),

    // ── Racks (paginated, filterable) ──
    listRacks: builder.query<PaginatedResponse<Rack>, ListParams>({
      query: (params = {}) => `racks/?${buildQuery(params)}`,
      providesTags: ['Rack'],
    }),
    createRack: builder.mutation<Rack, Partial<Rack>>({
      query: (body) => ({ url: 'racks/', method: 'POST', body }),
      invalidatesTags: ['Rack'],
    }),

    // ── Assets ──
    listDevices: builder.query<PaginatedResponse<Device>, ListParams>({
      query: (params = {}) => `devices/?${buildQuery(params)}`,
      providesTags: ['Device'],
    }),
    listServers: builder.query<PaginatedResponse<Server>, ListParams>({
      query: (params = {}) => `servers/?${buildQuery(params)}`,
      providesTags: ['Server'],
    }),
    createServer: builder.mutation<Server, Partial<Server>>({
      query: (body) => ({ url: 'servers/', method: 'POST', body }),
      invalidatesTags: ['Server', 'Device'],
    }),
    listSwitches: builder.query<PaginatedResponse<Switch>, ListParams>({
      query: (params = {}) => `switches/?${buildQuery(params)}`,
      providesTags: ['Switch'],
    }),
    listAppliances: builder.query<PaginatedResponse<Appliance>, ListParams>({
      query: (params = {}) => `appliances/?${buildQuery(params)}`,
      providesTags: ['Appliance'],
    }),

    // ── Users ──
    listUsers: builder.query<PaginatedResponse<User>, ListParams>({
      query: (params = {}) => `users/?${buildQuery(params)}`,
      providesTags: ['User'],
    }),

    // ── Audit logs ──
    listAuditLogs: builder.query<PaginatedResponse<AuditLog>, ListParams>({
      query: (params = {}) => `audit-logs/?${buildQuery(params)}`,
    }),
  }),
})

export const {
  useListRegionsQuery,
  useListAvailabilityZonesQuery,
  useListBuildingsQuery,
  useListFloorsQuery,
  useListRoomsQuery,
  useListRacksQuery,
  useCreateRackMutation,
  useListDevicesQuery,
  useListServersQuery,
  useCreateServerMutation,
  useListSwitchesQuery,
  useListAppliancesQuery,
  useListUsersQuery,
  useListAuditLogsQuery,
} = inventoryApi
