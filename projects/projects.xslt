<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" />
    <xsl:template match="/projects">
        <html>
        <body>
            <h2>Projects List</h2>
            <table border="1">
                <tr>
                    <th>Identifiant</th>
                    <th>Name</th>
                    <th>Duration</th>
                    <th>Size</th>
                    <th>Employee ID</th>
                    <th>Description</th>
                </tr>
                <xsl:for-each select="project">
                    <tr>
                        <td><xsl:value-of select="@identifiant" /></td>
                        <td><xsl:value-of select="name" /></td>
                        <td><xsl:value-of select="duree" /> (<xsl:value-of select="duree/@type" />)</td>
                        <td><xsl:value-of select="taille" /> (<xsl:value-of select="taille/@tailldeproject" />)</td>
                        <td><xsl:value-of select="idemp" /></td>
                        <td><xsl:value-of select="description" /></td>
                    </tr>
                </xsl:for-each>
            </table><br/>
          
        </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
