package org.example;

import org.junit.Before;
import org.junit.Test;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

import static org.junit.Assert.*;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.*;

public class SQLExecutorTest {

    private Connection mockConnection;
    private Statement mockStatement;
    private ResultSet mockResultSet;
    private SQLExecutor sqlExecutor;

    @Before
    public void setUp() throws SQLException {
        // 创建Mock对象
        mockConnection = mock(Connection.class);
        mockStatement = mock(Statement.class);
        mockResultSet = mock(ResultSet.class);

        // 配置Mock对象的行为
        when(mockConnection.createStatement()).thenReturn(mockStatement);
        when(mockStatement.executeQuery(anyString())).thenReturn(mockResultSet);

        // 创建SQLExecutor对象，注入mock的Connection
        sqlExecutor = new SQLExecutor(mockConnection);
    }

    @Test
    public void testExecuteSQL_SelectQuery() throws SQLException {
        // 调用executeSQL方法
        ResultSet result = sqlExecutor.executeSQL("SELECT * FROM table", "dbUrl", "username", "password");

        // 验证方法的行为
        verify(mockConnection).createStatement();
        verify(mockStatement).executeQuery("SELECT * FROM table");
        verify(mockConnection, never()).commit();

        // 验证结果
        assertNotNull(result);
    }

    @Test
    public void testExecuteSQL_NonSelectQuery() throws SQLException {
        // 调用executeSQL方法
        ResultSet result = sqlExecutor.executeSQL("UPDATE table SET column = value", "dbUrl", "username", "password");

        // 验证方法的行为
        verify(mockConnection).createStatement();
        verify(mockStatement, never()).executeQuery(anyString());
        verify(mockStatement).executeUpdate("UPDATE table SET column = value");
        verify(mockConnection).commit();

        // 验证结果
        assertNull(result);
    }

    @Test
    public void testExecuteSQL_ConnectionFailure()  {
        // 配置Mock对象以模拟连接失败
        SQLException expectedException = new SQLException("Connection failed");
        try {
            when(mockConnection.createStatement()).thenThrow(expectedException);
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }

        // 调用executeSQL方法
        ResultSet result = sqlExecutor.executeSQL("SELECT * FROM table","dbUrl", "username", "password" );

        // 验证结果
        assertNull(result);
    }

    @Test
    public void testExecuteSQL_InvalidStatement() {
        // 配置Mock对象以模拟执行无效SQL语句时的异常
        SQLException expectedException = new SQLException("Invalid SQL statement");
        try {
            when(mockStatement.executeQuery(anyString())).thenThrow(expectedException);
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }

        // 调用executeSQL方法
        ResultSet result = sqlExecutor.executeSQL("SELECT * FROM non_existent_table", "dbUrl", "username", "password");

        // 验证结果
        assertNull(result);
    }
}


