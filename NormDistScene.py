from manim import *
from scipy.stats import norm
import os

class NormDist(Scene):

    def construct(self):
        skip_animations = False

        # Declare PDF model
        class PDFPlot(VGroup):

            def __init__(self, mean, std):
                super().__init__()

                f = lambda x: norm.pdf(x, mean, std)

                self.mean = mean
                self.std = std
                self.lower_x = mean - std * 3
                self.upper_x = mean + std * 3

                axes = Axes(x_range=[self.lower_x, self.upper_x, std],
                            y_range=[0, f(mean) + .01, (f(mean) + .01) / 4],
                            x_axis_config={"include_numbers": True,
                                           "numbers_to_exclude": [mean - 4 * std]
                                           },
                            y_axis_config={"include_numbers": True,
                                           "decimal_number_config": {
                                               "num_decimal_places": 2
                                           }
                                           }
                            )

                plot = axes.plot(f, color=BLUE)
                self.add(axes, plot)

                self.f = f
                self.axes = axes
                self.plot = plot

            def x2p(self, x):
                return self.axes.c2p(x, self.f(x))

            def area_range(self, x_start, x_end, color=BLUE):
                return self.axes.get_area(self.plot, color=color, x_range=(x_start, x_end))

        #Write out the question and show it to the viewer
        question1 = Tex(r'Most IQ tests have a mean of 100 and a standard deviation of 15.', font_size=36)
        question2 = Tex(r'What is the probability that someone has an IQ greater than 115?', font_size=36)
        question_group = VGroup(question1, question2).arrange(DOWN).to_edge(UP)
        self.add(question_group)
        
        #can be set to any mean and standard deviation. This is based on the problem stated above.
        mean, std = 100, 15
        
        pdf_model = PDFPlot(mean, std)
        
        self.wait(3)
        
        #Show the normal distribution
        self.play(FadeIn(pdf_model))
        
        #Start the area from the lower boundry of the graph
        x_upper_tracker = ValueTracker(mean - std * 3)
        
        # Declare the area for the PDF which will update based on the trackers above
        area_color = BLUE
        area: Mobject = always_redraw(
            lambda: pdf_model.area_range(-3 * std + mean, x_upper_tracker.get_value(), color=area_color)
        )
        
        #How we look up the area. Equivilent to looking it up in a book or Excel
        cdf = lambda x: norm.cdf(x, mean, std)
        
        #Looks up the area to the left of 115 
        label_cdf = DecimalNumber(cdf(115), num_decimal_places=4)
        area_center = pdf_model.axes.c2p((115 + mean - 3*std) * 0.5, pdf_model.f(115) * .5)
        

        # fade in the label, move the PDF to x = 115
        self.add(area)
        self.play(x_upper_tracker.animate.set_value(115))
        self.wait()
    
        label_cdf.move_to(area_center)
        self.add(label_cdf)
        self.wait()
        
        #Create the area for the upper area that we want to find
        area_color_upper = RED
        x_lower_tracker = ValueTracker(mean + std*3)
        area2: Mobject = always_redraw(
            lambda: pdf_model.area_range(x_lower_tracker.get_value(), 3 * std + mean, color=area_color_upper)
        )
        
        #add this upper area to the scene and draw it from the right boundry of the distribution
        self.add(area2)
        self.play(x_lower_tracker.animate.set_value(115))
        
        self.wait()
        
        #Put a question mark because this is the area we're trying to find 
        red_area_center = pdf_model.axes.c2p(122, pdf_model.f(122)*0.5)
        question_mark = Tex("?").move_to(red_area_center)
        self.add(question_mark)
        
        self.wait()
        
        #Show that the entire area of the distribution is 1
        b = Brace(VGroup(area,area2), direction=[0.,1.,0.])
        b_text = b.get_text("1")
        self.add(b, b_text)
       
        self.wait()
        
        #Scale the current view down and move it off to the left
        group1 = VGroup(pdf_model, label_cdf, question_mark, b, b_text)
        
        self.play(group1.animate.scale(0.6).to_edge(LEFT))
        self.wait()
        
        #Make a copy of the red area and move it to the right
        group2 = VGroup(area2, question_mark).copy()
        
        self.play(group2.animate.scale(0.6).next_to(group1, RIGHT, 0.5).align_to(group1, UP))
        
        self.wait()
        
        #Add an equal sign 
        eq = MathTex("=").next_to(group2, RIGHT)
        self.play(FadeIn(eq))
        
        #Make a copy of the entire distribution and move it to the right side
        group3 = VGroup(group1, area, area2).copy()
        self.play(group3.animate.scale(0.6).next_to(group2, DOWN).align_to(group2, LEFT))
        
        #Make and show a minus sign
        minus = MathTex("-").next_to(group3, RIGHT)
        self.add(minus)
        
        #Make a copy of the blue area that we know and move it to the right
        group4 = VGroup(area, label_cdf).copy()
        self.play(group4.animate.scale(0.6).next_to(group3, DOWN).align_to(group2, LEFT))
        
        self.wait()
        
        #We can now replace these visualizations with mathematical symbols 
        x_text = MathTex("x").move_to(group2.get_center())
        whole_text = MathTex("1").move_to(group3.get_center())
        area_text = MathTex(str(round(label_cdf.get_value(),4))).move_to(group4.get_center())
        
        self.play(FadeIn(x_text, whole_text, area_text), FadeOut(group2, group3, group4))
        
        self.wait()
        
        #Show the full equation all together
        full_eq = MathTex(r'x = 1 - ' + str(round(label_cdf.get_value(),4))).move_to(whole_text.get_center())
        
        self.play(FadeOut(x_text, eq, whole_text, minus, area_text), FadeIn(full_eq))
        
        self.wait()
        
        #Display the answer
        answer = MathTex(str(round(1-label_cdf.get_value(),4))).next_to(full_eq,DOWN)
        self.play(FadeIn(answer))
        
        self.wait(5)
        
