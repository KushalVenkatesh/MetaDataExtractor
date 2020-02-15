library(shiny)
library(dplyr)
library(tidyverse)
library(shinythemes)
library(plotly)
library(shinythemes)
library(ggplot2)

ur_path <- glue::glue(getwd(), "/data/metadata.csv")
don <- read_csv(ur_path, col_types = list(col_double(), 
                                          col_character(), 
                                          col_datetime(), 
                                          col_character(), 
                                          col_datetime(), 
                                          col_character())) %>% 
  select(-X1) %>% 
  rename(authors = `Author(s)`,
         created_date = `Created Date`,
         last_mod_by = `Last Modified By`,
         modified_date = `Modified Date`,
         title = Title) %>% 
  na.omit()

cre <- don %>% 
  select(title, created_date, authors) %>% 
  rename(date = created_date, 
         author = authors)
mod <- don %>% 
  select(title,modified_date, last_mod_by) %>% 
  rename(date = modified_date, 
         author = last_mod_by)

viz_don <- cre %>% 
  rbind(mod)

people <- unique(viz_don$author)
files <- unique(viz_don$title)


ui <- fluidPage(theme = shinytheme('sandstone'),
                title = 'BlueTeam',
                
                navbarPage(tags$strong("Metadata Visualisation"),
                           
                           tabPanel('File tracker',
                                    sidebarPanel(
                                      selectInput('Files',
                                                  "Choose the files you're interested in!",
                                                  choices = files,
                                                  selected = "20190604_EDG_P26_BC_MAO International_JSOM",
                                                  multiple = TRUE),
                                      sliderInput('plotHeight',
                                                  'Adjust the height of the plot', 
                                                  min = 100,
                                                  max = 5000,
                                                  value = 900),
                                      sliderInput('plotWidth',
                                                  'Adjust the width of the plot',
                                                  min = 100,
                                                  max = 5000,
                                                  value = 1200)),
                                    mainPanel(plotlyOutput("filemetadata", width = "150%", height = "20%"),
                                              DT::dataTableOutput(outputId = "filetable"))
                ),
                tabPanel('People tracker',
                         sidebarPanel(
                           selectInput('Author',
                                       "Choose the people you're interested in!",
                                       choices = people,
                                       selected = "Mourier CPL",
                                       multiple = TRUE),
                           sliderInput('plotHeight2',
                                       'Adjust the height of the plot', 
                                       min = 100,
                                       max = 5000,
                                       value = 900),
                           sliderInput('plotWidth2',
                                       'Adjust the width of the plot',
                                       min = 100,
                                       max = 5000,
                                       value = 1200)),
                         mainPanel(plotlyOutput("peoplemetadata", width = "150%", height = "20%"),
                                   DT::dataTableOutput(outputId = "peopletable"))
                )
)
)





# Define server logic
server <- function(input, output) {
  
  ################### FILE METADATA ######################
  
  # file_data <- reactive({
  #   don %>%
  #     filter(title %in% input$Files & last_mod_by %in% input$Author & authors %in% input$Author)
  # })
  
  file_data_viz <- reactive({
    viz_don %>%
      filter(title %in% input$Files)
  })
  
  # output$filemetadata <- renderPlotly({
  #   p <- ggplot(data = file_data(),
  #               aes_string(y = as.factor(file_data()$title),
  #                          x = file_data()$created_date,
  #                          color = as.factor(file_data()$authors))) +
  #     geom_point() +
  #     geom_line(group = as.factor(file_data()$authors)) +
  #     geom_point(aes_string(y = as.factor(file_data()$title),
  #                           x = file_data()$modified_date,
  #                           color = as.factor(file_data()$last_mod_by),
  #                           group = as.factor(file_data()$last_mod_by))) +
  #     geom_line(aes_string(y = as.factor(file_data()$title),
  #                          x = file_data()$modified_date,
  #                          color = as.factor(file_data()$last_mod_by),
  #                          group = as.factor(file_data()$last_mod_by))) +
  #     theme_bw() +
  #     xlab("Date") +
  #     ggtitle("File metadata tracking") +
  #     theme(axis.text.y = element_text(angle = 45))
  #   
  #   ggplotly(p,
  #            height = input$plotHeight,
  #            width = input$plotWidth,
  #            opacity = 0.6)
  # })
  
  output$filemetadata <- renderPlotly({
    p <- ggplot(data = file_data_viz(),
                aes_string(y = as.factor(file_data_viz()$title),
                           x = file_data_viz()$date,
                           color = as.factor(file_data_viz()$author),
                           group = as.factor(file_data_viz()$title),
                           size=2,
                           alpha = 0.6)) +
      geom_point() +
      geom_line() +
      theme_bw() +
      xlab("Date") +
      ggtitle("File metadata tracking") +
      theme(axis.text.y = element_blank())
    
    ggplotly(p,
             height = input$plotHeight,
             width = input$plotWidth,
             opacity = 0.6)
  })
  
  output$filetable <- DT::renderDataTable({
    don %>%
      filter(title %in% input$Files)
  })
  
  ################### PEOPLE METADATA ######################
  
  people_data_viz <- reactive({
    viz_don %>%
      filter(author %in% input$Author)
  })
  
  output$peoplemetadata <- renderPlotly({
    pp <- ggplot(data = people_data_viz(),
                aes_string(y = as.factor(people_data_viz()$title),
                           x = people_data_viz()$date,
                           color = as.factor(people_data_viz()$author),
                           group = as.factor(people_data_viz()$title),
                           size=2,
                           alpha = 0.6)) +
      geom_point() +
      geom_line() +
      theme_bw() +
      xlab("Date") +
      ggtitle("File metadata tracking") +
      theme(axis.text.y = element_blank())
    
    ggplotly(pp,
             height = input$plotHeight2,
             width = input$plotWidth2,
             opacity = 0.6)
  })
  
  output$peopletable <- DT::renderDataTable({
    don %>%
      filter(last_mod_by %in% input$Author & authors %in% input$Author)
  })

}

# Run the application 
shinyApp(ui = ui, server = server)