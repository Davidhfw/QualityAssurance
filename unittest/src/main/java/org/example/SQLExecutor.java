package org.example;

import java.sql.*;

public class SQLExecutor {
    /**
     * 执行SQL查询并返回结果。
     *
     * @param sqlQuery SQL查询语句
     * @param dbUrl    PostgreSQL数据库连接URL
     * @param username 数据库用户名
     * @param password 数据库密码
     * @return 查询结果的List，如果是SELECT语句;否则返回null
     */
    public static ResultSet executeSQL(String sqlQuery, String dbUrl, String username, String password) {
        try {
            // 连接到PostgreSQL数据库
            Connection conn = DriverManager.getConnection(dbUrl, username, password);
            Statement stmt = conn.createStatement();

            // 执行SQL查询
            if (sqlQuery.startsWith("SELECT")) {
                return stmt.executeQuery(sqlQuery);
            } else {
                stmt.executeUpdate(sqlQuery);
                conn.commit();
                return null;
            }
        } catch (SQLException e) {
            System.out.println("Error occurred: " + e.getMessage());
            return null;
        }
    }
}
