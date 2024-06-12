<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" />
    <xsl:template match="/Employers">
        <html>
        <body>
            <h2>Employees List</h2>
            <table border="1">
                <tr>
                    <th>CIN</th>
                    <th>Name</th>
                    <th>Sexe</th>
                    <th>Age</th>
                    <th>Phone</th>
                    <th>Email</th>
                </tr>
                <xsl:for-each select="Persone">
                    <tr>
                        <td><xsl:value-of select="CIN" /></td>
                        <td><xsl:value-of select="name" /></td>
                        <td><xsl:value-of select="sexe/@type" /></td>
                        <td><xsl:value-of select="age" /></td>
                        <td><xsl:value-of select="phone" /></td>
                        <td><xsl:value-of select="email" /></td>
                    </tr>
                </xsl:for-each>
            </table>
            
        </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
