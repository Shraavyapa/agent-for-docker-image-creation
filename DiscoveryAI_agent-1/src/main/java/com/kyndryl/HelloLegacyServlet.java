package com.example.legacy;

import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.DriverManager;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

@WebServlet(name = "HelloServlet", urlPatterns = {"/hello", "/api/hello"})
public class HelloLegacyServlet extends HttpServlet {
    
    // Database connection string - for agent to detect
    private static final String DB_URL = "jdbc:postgresql://localhost:5432/legacydb";
    private static final String DB_USER = "admin";
    private static final String DB_PASSWORD = "password";

    @Override
    protected void doGet(HttpServletRequest request,
                         HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/html");
        PrintWriter out = response.getWriter();
        out.println("<html>");
        out.println("<head><title>Simple Legacy App</title></head>");
        out.println("<body>");
        out.println("<h1>Hello from a simple legacy Java servlet!</h1>");
        out.println("<p>This app is a demo version for PE.</p>");
        out.println("<p>Database: " + DB_URL + "</p>");
        out.println("</body>");
        out.println("</html>");
    }
    
    @Override
    protected void doPost(HttpServletRequest request,
                          HttpServletResponse response)
            throws ServletException, IOException {
        // POST endpoint for creating data
        response.setContentType("application/json");
        PrintWriter out = response.getWriter();
        out.println("{\"status\": \"success\", \"message\": \"Data created\"}");
    }
}
