library(tidyverse)
library(shiny)
library(tidyr)
library(shinydashboard)
library(shinyalert)


ui <- dashboardPage(
  skin = 'blue',
  dashboardHeader(title = "Google Flights Analysis"),
  dashboardSidebar(
    # side menu items
    sidebarMenu(
      menuItem("Overview",
               tabName = "overview")
    )
  ),
  dashboardBody(
    tabItems(
      #overview
      tabItem(
        tabName = "overview",
        h1("Analyzing Flights"),
        p("Using data science algorithms and methods to analyze and track flight prices over time.")
      )
    )
  )
)

server <- function(input, output, session) {
  
}

shinyApp(ui, server)