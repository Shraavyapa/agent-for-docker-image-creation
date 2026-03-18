package com.example.legacy;

import java.io.IOException;
import java.io.PrintWriter;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

public class HelloLegacyServlet extends HttpServlet {

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
        out.println("</body>");
        out.println("</html>");
    }
}
