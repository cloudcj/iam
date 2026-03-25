import { configureStore } from '@reduxjs/toolkit'
import { iamApi } from '../services/iamApi'

export const store = configureStore({
  reducer: {
    [iamApi.reducerPath]: iamApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(iamApi.middleware),
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
