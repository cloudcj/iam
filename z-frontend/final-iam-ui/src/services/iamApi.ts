import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import type { FetchArgs, FetchBaseQueryError } from '@reduxjs/toolkit/query'
import type { User, Role, Permission, Department, Me, LoginRequest, CreateUserPayload } from '../types'

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
  tagTypes: ['User', 'Role', 'Permission', 'Department', 'Me'],
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
    getUser: builder.query<User, string>({
      query: (id) => `/identity/users/${id}/`,
      providesTags: ['User'],
    }),
    createUser: builder.mutation<User, CreateUserPayload>({
      query: (body) => ({ url: '/identity/users/create/', method: 'POST', body }),
      invalidatesTags: ['User'],
    }),
    updateUser: builder.mutation<User, { id: string; body: Partial<User> }>({
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

    // Departments
    getDepartments: builder.query<Department[], void>({
      query: () => '/identity/departments/',
      providesTags: ['Department'],
    }),
    createDepartment: builder.mutation<Department, Partial<Department>>({
      query: (body) => ({ url: '/identity/departments/', method: 'POST', body }),
      invalidatesTags: ['Department'],
    }),
    updateDepartment: builder.mutation<Department, { id: string; body: Partial<Department> }>({
      query: ({ id, body }) => ({ url: `/identity/departments/${id}/`, method: 'PATCH', body }),
      invalidatesTags: ['Department'],
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
  useGetDepartmentsQuery,
  useCreateDepartmentMutation,
  useUpdateDepartmentMutation,
  useDeleteUserMutation,
} = iamApi
