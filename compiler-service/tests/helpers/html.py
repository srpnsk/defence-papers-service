# tests/helpers/html.py

def generate_simple_html(title: str, text: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
    </head>
    <body>
        <h1>{title}</h1>
        <p>{text}</p>
    </body>
    </html>
    """


def generate_html_with_table() -> str:
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
    </head>
    <body>
        <h1>Table</h1>

        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Value</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>First</td>
                    <td>100</td>
                </tr>
                <tr>
                    <td>Second</td>
                    <td>200</td>
                </tr>
            </tbody>
        </table>
    </body>
    </html>
    """


def generate_html_with_cyrillic() -> str:
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
    </head>
    <body>
        <h1>Диссертационный совет</h1>
        <p>Документ успешно сгенерирован.</p>
    </body>
    </html>
    """
