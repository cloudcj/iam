# IAM Pagination Reference

This document describes the pagination strategies used across the IAM system and provides examples for frontend integration.

## Overview

The IAM system uses **page-based pagination** for all endpoints (`CustomPagination`):

| Endpoint | Query Params | Default | Max |
|----------|--------------|---------|-----|
| **User List** | `page`, `per_page` | 10 items/page | 100 items/page |
| **Audit Logs** | `page`, `per_page` | 10 items/page | 100 items/page |

Simple, consistent, and efficient for datasets < 100k records.

---

## Page-Based Pagination (CustomPagination)

Used by: `GET /api/v1/identity/users/` and `GET /api/v1/audit/logs/`

### Query Parameters

| Parameter | Type | Default | Max | Description |
|-----------|------|---------|-----|-------------|
| `page` | integer | 1 | N/A | Page number (1-indexed) |
| `per_page` | integer | 10 | 100 | Items per page |

### Request Examples

```bash
# Get page 1 with default 10 items
GET /api/v1/identity/users/

# Get page 3 with 25 items per page
GET /api/v1/identity/users/?page=3&per_page=25

# With filters
GET /api/v1/identity/users/?page=2&per_page=50&is_active=true&department=uuid-here
```

### Response Format

```json
{
  "page": 2,
  "per_page": 10,
  "num_pages": 5,
  "count": 50,
  "next": "http://localhost:8000/api/v1/identity/users/?page=3&per_page=10",
  "previous": "http://localhost:8000/api/v1/identity/users/?page=1&per_page=10",
  "results": [
    {
      "id": "uuid-1",
      "username": "john.doe",
      "email": "john.doe@example.com",
      ...
    },
    ...
  ]
}
```

### Frontend Usage Example

```typescript
// React/TypeScript example
const [page, setPage] = useState(1);
const [perPage, setPerPage] = useState(10);

const fetchUsers = async () => {
  const response = await fetch(
    `/api/v1/identity/users/?page=${page}&per_page=${perPage}`
  );
  const data = await response.json();
  
  return {
    users: data.results,
    totalPages: data.num_pages,
    totalCount: data.count,
    currentPage: data.page,
  };
};
```

---

## Audit Log Filters

Additional query parameters available for `/api/v1/audit/logs/`:

| Parameter | Type | Description |
|-----------|------|-------------|
| `action` | string | Exact action code (e.g., `user.create`, `user.delete`) |
| `action_category` | string | `auth` or `activity` (groups actions by prefix) |
| `status` | string | `success` or `failure` |
| `actor_id` | UUID | User ID who performed the action |
| `target_type` | string | Type of resource affected (e.g., `user`, `role`) |
| `date_from` | date | Start date (YYYY-MM-DD) |
| `date_to` | date | End date (YYYY-MM-DD) |

### Audit Log Response Example

```json
{
  "page": 1,
  "per_page": 10,
  "num_pages": 125,
  "count": 1250,
  "next": "http://localhost:8000/api/v1/audit/logs/?page=2",
  "previous": null,
  "results": [
    {
      "id": "uuid-1",
      "actor": "admin.user",
      "actor_name": "Admin User",
      "department": "GLOBAL",
      "action": "user.create",
      "target_id": "uuid-target",
      "target_type": "user",
      "status": "success",
      "detail": "{\"username\": \"john.doe\"}",
      "ip_address": "192.168.1.100",
      "timestamp": "2026-04-06T14:30:00Z"
    },
    ...
  ]
}
```

### Audit Logs Frontend Example

```typescript
// React/TypeScript example
const [page, setPage] = useState(1);
const [logs, setLogs] = useState([]);

const fetchAuditLogs = async (pageNum: number) => {
  const response = await fetch(
    `/api/v1/audit/logs/?page=${pageNum}&per_page=10&action_category=activity`
  );
  const data = await response.json();
  
  return {
    logs: data.results,
    totalPages: data.num_pages,
    totalCount: data.count,
    currentPage: data.page,
  };
};
```

---

## Design Decisions

### Unified Pagination Strategy

All endpoints use **page-based pagination** (`CustomPagination`):
- ✅ Simple, consistent API across all endpoints
- ✅ Efficient for datasets < 100k records
- ✅ Matches frontend page navigation UI
- ✅ Easy to understand and implement
- ✅ DRF built-in, well-tested

### Performance Implications

**Page-Based scalability:**
- Efficient for datasets < 100k records (current system size)
- DRF pagination handles internally with SQL `LIMIT` + `OFFSET`
- For > 1M records: consider upgrading to cursor-based pagination (see Future Improvements)
- Current implementation: no performance concerns for expected audit log volume

---

## Common Patterns

### Implementing Page Navigation

```typescript
// Works for both users list and audit logs
const goToPage = async (pageNum: number) => {
  const response = await fetch(
    `/api/v1/identity/users/?page=${pageNum}&per_page=10`
  );
  const data = await response.json();
  
  return {
    items: data.results,
    currentPage: data.page,
    totalPages: data.num_pages,
    totalCount: data.count,
    hasNext: data.next !== null,
    hasPrev: data.previous !== null,
  };
};
```

### Combining Filters with Pagination (Audit Logs)

```typescript
const fetchAuditWithFilters = async (page: number, filters: any) => {
  const params = new URLSearchParams({
    page: String(page),
    per_page: "10",
    action_category: filters.category,
    status: filters.status,
    date_from: filters.dateFrom,
    date_to: filters.dateTo,
  });
  
  const response = await fetch(`/api/v1/audit/logs/?${params}`);
  return response.json();
};
```

---

## Error Handling

### Invalid Parameters

Endpoints handle invalid query parameters gracefully:

```bash
# Invalid per_page (too large) → capped to max 100
GET /api/v1/identity/users/?per_page=500  # → treated as per_page=100

# Non-integer page → defaults to page 1
GET /api/v1/identity/users/?page=abc  # → treated as page=1

# Out-of-range page → empty results (no error)
GET /api/v1/identity/users/?page=999
```

### Recommended Client-Side Validation

```typescript
const validatePagination = (page: number, perPage: number) => {
  if (page < 1) throw new Error("Page must be >= 1");
  if (perPage < 1 || perPage > 100) {
    throw new Error("Per page must be 1-100");
  }
};
```

---

## Testing

### Sample Test URLs

**Users List:**
```
http://localhost:8000/api/v1/identity/users/?page=1&per_page=10
http://localhost:8000/api/v1/identity/users/?page=1&per_page=10&is_active=true
http://localhost:8000/api/v1/identity/users/?page=1&per_page=10&search=john
```

**Audit Logs:**
```
http://localhost:8000/api/v1/audit/logs/?page=1&per_page=10
http://localhost:8000/api/v1/audit/logs/?page=1&per_page=10&action_category=activity
http://localhost:8000/api/v1/audit/logs/?page=1&per_page=50&status=failure&date_from=2026-04-01
```

---

## Future Improvements

### When Scale Changes (> 100k records)

If audit logs exceed 100k records in the future, consider:
1. **Cursor-Based Pagination**: Migrate to cursor-based pagination for O(1) performance (no DB scan)
2. **OffsetLimitPagination**: Upgrade path already built in `apps/common/pagination.py` (ready to use)
3. **Database Indexing**: Add indexes on `timestamp` + `id` for efficient log queries

### Other Optimizations

1. **Response Compression**: Consider gzip for large result sets
2. **Caching**: Add cache headers for read-heavy endpoints
3. **Real-time Updates**: WebSocket support for live audit log streaming

---

## Questions & Support

For questions about pagination or API integration, refer to the main [IAM-design-decisions.md](IAM-design-decisions.md) document or contact the backend team.
