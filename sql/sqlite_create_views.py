import sqlite3

connection = sqlite3.connect("../prices.db")

c = connection.cursor()

c.execute("DROP VIEW IF EXISTS vw_price_change;")
c.execute("DROP VIEW IF EXISTS vw_prices_products;")
c.execute("DROP VIEW IF EXISTS vw_user_product_tracking;")

c.execute(
        """
        CREATE VIEW vw_price_change
        AS
        SELECT pp.ID,
               pp.Product,
            pp.CurrentPrice,
            pp.PreviousPrice,
            pp.ProductURL,
            DATE(pp.Date, 'unixepoch', 'localtime') as Date
        FROM
            (
            SELECT DISTINCT
                prod.ID,
                prod.Product,
                prod.ProductURL,
                rn.Date,
                MAX
                    (
                    CASE
                        WHEN rn.RN_PRICE = 1
                            THEN rn.Price
                        ELSE NULL
                    END
                    )
                    OVER(PARTITION BY rn.ProductID) AS "CurrentPrice",
                MAX
                    (
                    CASE
                        WHEN rn.RN_PRICE = 2
                            THEN rn.Price
                        ELSE NULL
                    END
                    )
                    OVER(PARTITION BY rn.ProductID) AS "PreviousPrice"
            FROM
                (
                SELECT ProductID,
                    Price,
                    Date,
                    ROW_NUMBER()
                        OVER(PARTITION BY ProductID ORDER BY Date DESC) AS "RN_PRICE"
                FROM prices
                ) rn
            INNER JOIN products prod
                ON rn.ProductID = prod.ID
            WHERE rn.RN_PRICE BETWEEN 1 AND 2
            ) pp
        WHERE pp.PreviousPrice IS NOT NULL
        ORDER BY Date DESC;
        """
)

c.execute(
        """
        CREATE VIEW vw_prices_products as
        SELECT v.Vendor, p.Product, pr.Price, DATE(pr.Date, 'unixepoch', 'localtime') as Date, p.ProductURL
                        FROM prices pr
                        INNER JOIN vendors v ON pr.VendorID = v.ID
                        INNER JOIN products p ON pr.ProductID = p.ID
        ORDER BY Date DESC;
        """
)

c.execute(
        """
        CREATE VIEW vw_user_product_tracking
        AS
        SELECT ProductID, Name, Email, Product, ProductURL
        FROM tracking
        INNER JOIN users u on u.ID = tracking.UserID
        INNER JOIN products p on tracking.ProductID = p.ID
        """
)

connection.close()
