import mysql.connector
global connection

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='DBMS',
    database='chatbot_dialogue_flow'
)


def get_next_order_id():
    cursor = connection.cursor()
    query = ("SELECT MAX(order_id) FROM orders")
    cursor.execute(query)

    result = cursor.fetchone()[0]

    cursor.close()

    if result is None:
        return 1
    else:
        return result + 1


def insert_order_item(food_item: str, quantity: int, order_id: int):
    try:
        cursor = connection.cursor()
        cursor.callproc('insert_order_item', (food_item, quantity, order_id))
        connection.commit()
        cursor.close()
        print('Order item inserted successfully!')

        return 1

    except mysql.connector.Error as err:
        print(f'Error inserting order item: {err}')
        # Roll back changes if necessary
        connection.rollback()

        return -1

    except Exception as e:
        print(f'An error occurred: {e}')
        # Roll back changes if necessary
        connection.rollback()

        return -1


def get_total_order_price(order_id: int):
    cursor = connection.cursor()
    query = f'SELECT get_total_order_price({order_id})'
    cursor.execute(query)
    result = cursor.fetchone()[0]
    cursor.close()
    return result


def insert_order_tracking_status(order_id: int, status: str):
    cursor = connection.cursor()
    query = f'insert into order_tracking (order_id, status) values(%s, %s)'
    cursor.execute(query, (order_id, status))
    connection.commit()
    cursor.close()


def get_order_status(order_id: int):
    cursor = connection.cursor()
    query = ("SELECT status FROM order_tracking where order_id = %s")
    cursor.execute(query, (order_id, ))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    if result is not None:
        return result[0]
    else:
        return None
