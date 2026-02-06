{
  "user": {
    "id": "user-123",
    "username": "cj"
  },
  "systems": {
    "inventory": {
      "permissions": [
        "inventory.access",
        "inventory.dashboard.view",
        "inventory.products.view",
        "inventory.stock.adjust"
      ],
      "menu": [
        {
          "key": "dashboard",
          "label": "Dashboard",
          "path": "/inventory/dashboard",
          "permission": "inventory.dashboard.view",
          "order": 1
        },
        {
          "key": "products",
          "label": "Products",
          "path": "/inventory/products",
          "permission": "inventory.products.view",
          "order": 2
        }
      ]
    }
  }
}

#######################

class InventoryPermissions:
    # SYSTEM ACCESS
    ACCESS = "inventory.access"

    # MENU (VIEW)
    DASHBOARD_VIEW = "inventory.dashboard.view"
    PRODUCTS_VIEW = "inventory.products.view"
    STOCK_VIEW = "inventory.stock.view"
    REPORTS_VIEW = "inventory.reports.view"

    # ACTIONS
    PRODUCT_CREATE = "inventory.products.create"
    PRODUCT_UPDATE = "inventory.products.update"
    PRODUCT_DELETE = "inventory.products.delete"
    STOCK_ADJUST = "inventory.stock.adjust"

    VIEW_ALL = [
        DASHBOARD_VIEW,
        PRODUCTS_VIEW,
        STOCK_VIEW,
        REPORTS_VIEW,
    ]

    ACTION_ALL = [
        PRODUCT_CREATE,
        PRODUCT_UPDATE,
        PRODUCT_DELETE,
        STOCK_ADJUST,
    ]

    ALL = [
        ACCESS,
        *VIEW_ALL,
        *ACTION_ALL,
    ]
