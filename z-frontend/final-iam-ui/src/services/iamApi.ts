import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import type { FetchArgs, FetchBaseQueryError } from '@reduxjs/toolkit/query'
import type { User, UserDetail, Role, Permission, Policy, Department, Me, LoginRequest, CreateUserPayload, UpdateUserPayload, AuditLogParams, AuditLogResponse  } from '../types'

const getCsrfToken = () =>
  document.cookie
    .split('; ')
    .find((row) => row.startsWith('csrftoken='))
    ?.split('=')[1]

const baseQuery = fetchBaseQuery({
  baseUrl: '/api/v1',
  credentials: 'include',
  prepareHeaders: (headers) => {
    const csrf = getCsrfToken()
    if (csrf) headers.set('X-CSRFToken', csrf)
    return headers
  },
})

const baseQueryWithReauth = async (
  args: string | FetchArgs,
  api: any,
  extraOptions: any
) => {
  let result = await baseQuery(args, api, extraOptions)

  if (result.error && (result.error as FetchBaseQueryError).status === 401) {
    // Try to refresh the access token
    const refreshResult = await baseQuery(
      { url: '/auth/refresh/', method: 'POST' },
      api,
      extraOptions
    )

    if (refreshResult.data) {
      // Token refreshed — retry the original request
      result = await baseQuery(args, api, extraOptions)
    }
    // Refresh failed — return the 401 error as-is.
    // ProtectedRoute handles the redirect when useGetMeQuery returns no data.
    // Do NOT invalidateTags here — that causes an infinite refetch loop.
  }

  return result
}

export const iamApi = createApi({
  reducerPath: 'iamApi',
  baseQuery: baseQueryWithReauth,
  tagTypes: ['User', 'Role', 'Permission', 'Department', 'Me', 'AuditLog'],
  endpoints: (builder) => ({

    // Auth
    getCsrf: builder.query<void, void>({
      query: () => '/auth/csrf/',
    }),
    getMe: builder.query<Me, void>({
      query: () => '/me/',
      providesTags: ['Me'],
    }),
    login: builder.mutation<{ user: Me }, LoginRequest>({
      query: (credentials) => ({
        url: '/auth/login/',
        method: 'POST',
        body: credentials,
      }),
      invalidatesTags: ['Me'],
    }),
    logout: builder.mutation<void, void>({
      query: () => ({ url: '/auth/logout/', method: 'POST' }),
      invalidatesTags: ['Me'],
    }),

    // Users
    getUsers: builder.query<User[], void>({
      query: () => '/identity/users/',
      providesTags: ['User'],
    }),
    getUser: builder.query<UserDetail, string>({
      query: (id) => `/identity/users/${id}/`,
      providesTags: ['User'],
    }),

    createUser: builder.mutation<User, CreateUserPayload>({
      query: (body) => ({ url: '/identity/users/create/', method: 'POST', body }),
      invalidatesTags: ['User'],
    }),
    updateUser: builder.mutation<User, { id: string; body: UpdateUserPayload }>({
      query: ({ id, body }) => ({ url: `/identity/users/${id}/update/`, method: 'PATCH', body }),
      invalidatesTags: ['User'],
    }),
    deleteUser: builder.mutation<void, string>({
      query: (id) => ({ url: `/identity/users/${id}/delete/`, method: 'DELETE' }),
      invalidatesTags: ['User'],
    }),


    // Roles
    getRoles: builder.query<Role[], void>({
      query: () => '/access/roles/',
      providesTags: ['Role'],
    }),
    createRole: builder.mutation<Role, Partial<Role>>({
      query: (body) => ({ url: '/access/roles/', method: 'POST', body }),
      invalidatesTags: ['Role'],
    }),

    // Permissions
    getPermissions: builder.query<Permission[], void>({
      query: () => '/access/permissions/',
      providesTags: ['Permission'],
    }),

    // Policies
    getPolicies: builder.query<Policy[], void>({
      query: () => '/access/policies/',
      providesTags: ['Permission'],
    }),

    resetUserPassword: builder.mutation<{ detail: string }, { id: string; body: { new_password: string; confirm_password: string } }>({
      query: ({ id, body }) => ({ url: `/identity/users/${id}/reset-password/`, method: 'POST', body }),
    }),

    // Me — profile
    updateProfile: builder.mutation<{ first_name: string; last_name: string; email: string }, { first_name: string; last_name: string; email: string }>({
      query: (body) => ({ url: '/me/profile/', method: 'PATCH', body }),
      invalidatesTags: ['Me'],
    }),
    changePassword: builder.mutation<{ detail: string }, { current_password: string; new_password: string; confirm_password: string }>({
      query: (body) => ({ url: '/me/change-password/', method: 'POST', body }),
    }),

    // Departments
    getDepartments: builder.query<Department[], void>({
      query: () => '/department/',
      providesTags: ['Department'],
    }),
    createDepartment: builder.mutation<Department, { name: string; allowed_systems: string[] }>({
      query: (body) => ({ url: '/department/create/', method: 'POST', body }),
      invalidatesTags: ['Department'],
    }),
    updateDepartment: builder.mutation<Department, { id: string; body: { name: string; allowed_systems: string[] } }>({
      query: ({ id, body }) => ({ url: `/department/${id}/update/`, method: 'PATCH', body }),
      invalidatesTags: ['Department'],
    }),
    deleteDepartment: builder.mutation<void, string>({
      query: (id) => ({ url: `/department/${id}/delete/`, method: 'DELETE' }),
      invalidatesTags: ['Department'],
    }),

    // Audit
    getAuditLogs: builder.query<AuditLogResponse, AuditLogParams>({
      query: (params) => ({ url: '/audit/', params }),
      providesTags: ['AuditLog'],
    }),

  }),
})

export const {
  useGetCsrfQuery,
  useGetMeQuery,
  useLoginMutation,
  useLogoutMutation,
  useGetUsersQuery,
  useGetUserQuery,
  useCreateUserMutation,
  useUpdateUserMutation,
  useGetRolesQuery,
  useCreateRoleMutation,
  useGetPermissionsQuery,
  useGetPoliciesQuery,
  useGetDepartmentsQuery,
  useCreateDepartmentMutation,
  useUpdateDepartmentMutation,
  useDeleteDepartmentMutation,
  useDeleteUserMutation,
  useUpdateProfileMutation,
  useChangePasswordMutation,
  useResetUserPasswordMutation,
  useGetAuditLogsQuery 
} = iamApi

