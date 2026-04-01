import { configureStore } from '@reduxjs/toolkit'
import { iamApi } from '../services/iamApi'
import { inventoryApi } from '../services/inventoryApi'

export const store = configureStore({
  reducer: {
    [iamApi.reducerPath]: iamApi.reducer,
    [inventoryApi.reducerPath]: inventoryApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(iamApi.middleware, inventoryApi.middleware),
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
