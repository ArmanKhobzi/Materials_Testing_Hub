import streamlit as st
import plotly.graph_objects as go

class MaterialsTestingHub:
    def __init__(self):
        # User selections for the first set
        self.add_temperature = self.get_temperature("Set 1: ")
        self.add_humidity = self.get_humidity("Set 1: ")
        self.add_exercise = self.get_exercise("Set 1: ")

        # User selections for the second set
        self.add_temperature_2 = self.get_temperature("Set 2: ")
        self.add_humidity_2 = self.get_humidity("Set 2: ")
        self.add_exercise_2 = self.get_exercise("Set 2: ")

        # Importance levels for radar charts
        self.importance_levels = self.get_importance_levels(
            self.add_temperature, self.add_humidity, self.add_exercise
        )
        self.importance_levels_2 = self.get_importance_levels(
            self.add_temperature_2, self.add_humidity_2, self.add_exercise_2
        )

        # Display radar charts and popovers
        self.display_radar_charts()
        self.display_popovers()

    def get_temperature(self, label):
        return st.selectbox(
            f"{label}What is your target temperature?",
            ["Choose an option", "> 25°C", "10°C - 25°C", "< 10°C"],
            index=0,
            key=f"{label}_temperature"
        )

    def get_humidity(self, label):
        return st.selectbox(
            f"{label}What is your target humidity?",
            ["Choose an option", "> 60% RH", "< 40% RH"],
            index=0,
            key=f"{label}_humidity"
        )

    def get_exercise(self, label):
        return st.selectbox(
            f"{label}What is your exercise level?",
            ["Choose an option", "High", "Low to Rest"],
            index=0,
            key=f"{label}_exercise"
        )

    def get_importance_levels(self, temperature, humidity, exercise):
        # Default values if "Choose an option" is selected
        if temperature == "Choose an option" or humidity == "Choose an option" or exercise == "Choose an option":
            return {"Insulation": 3, "Breathability": 3, "Moisture Management": 3, "Thermal Hand": 3, "Density": 3}
        lookup = {
            # High temperature conditions
            ("> 25°C", "> 60% RH", "High"): {"Insulation": 1, "Breathability": 5, "Moisture Management": 5, "Thermal Hand": 3, "Density": 2},
            ("> 25°C", "> 60% RH", "Low to Rest"): {"Insulation": 1, "Breathability": 4, "Moisture Management": 2, "Thermal Hand": 3, "Density": 2},
            ("> 25°C", "< 40% RH", "High"): {"Insulation": 1, "Breathability": 5, "Moisture Management": 4, "Thermal Hand": 3, "Density": 2},
            ("> 25°C", "< 40% RH", "Low to Rest"): {"Insulation": 1, "Breathability": 3, "Moisture Management": 2, "Thermal Hand": 3, "Density": 2},
    
            # Medium temperature conditions
            ("10°C - 25°C", "> 60% RH", "High"): {"Insulation": 2.5, "Breathability": 5, "Moisture Management": 4, "Thermal Hand": 3, "Density": 2},
            ("10°C - 25°C", "> 60% RH", "Low to Rest"): {"Insulation": 2.5, "Breathability": 3, "Moisture Management": 2.5, "Thermal Hand": 3, "Density": 2},
            ("10°C - 25°C", "< 40% RH", "High"): {"Insulation": 2.5, "Breathability": 4, "Moisture Management": 5, "Thermal Hand": 3, "Density": 2.5},
            ("10°C - 25°C", "< 40% RH", "Low to Rest"): {"Insulation": 2.5, "Breathability": 2.5, "Moisture Management": 2, "Thermal Hand": 3, "Density": 2.5},
    
            # Low temperature conditions
            ("< 10°C", "> 60% RH", "High"): {"Insulation": 4, "Breathability": 5, "Moisture Management": 5, "Thermal Hand": 2.5, "Density": 3},
            ("< 10°C", "> 60% RH", "Low to Rest"): {"Insulation": 4, "Breathability": 2.5, "Moisture Management": 2, "Thermal Hand": 4, "Density": 3},
            ("< 10°C", "< 40% RH", "High"): {"Insulation": 4, "Breathability": 4, "Moisture Management": 5, "Thermal Hand": 2.5, "Density": 3},
            ("< 10°C", "< 40% RH", "Low to Rest"): {"Insulation": 4, "Breathability": 2.5, "Moisture Management": 2, "Thermal Hand": 2, "Density": 2},
        }
    
        # Default importance levels for unknown combinations
        return lookup.get((temperature, humidity, exercise), {
            "Insulation": 3, "Breathability": 3, "Moisture Management": 3, "Thermal Hand": 3, "Density": 3
        })

    def display_radar_charts(self):
        st.markdown("### Radar Charts of Importance Levels")
        col1, col2 = st.columns(2)

        with col1:
            self.display_radar_chart(self.importance_levels, "Radar Chart 1")
        with col2:
            self.display_radar_chart(self.importance_levels_2, "Radar Chart 2")

    def display_radar_chart(self, importance_levels, title):
        labels = list(importance_levels.keys())
        values = list(importance_levels.values())

        # Close the radar chart by appending the first point again
        labels.append(labels[0])
        values.append(values[0])

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=values, theta=labels, fill='toself', name=title))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
            showlegend=False
        )
        st.plotly_chart(fig)

    def display_popovers(self):
        st.markdown("## Materials Features")
        
        with st.expander("Insulation"):
            if st.checkbox("Thermal Insulation (Resistance)"):
                st.markdown("**Metric**: Thermal resistance RCF, a quantity specific to textile materials or composites, determines the dry heat flux across a given area in response to a steady applied temperature gradient.")
                st.markdown("**Relevant Standard**: Sweating Guarded Hot Plate - **ASTM** **F1868 - Part A**")
                st.markdown("**Sample Size**: 30cm X 30cm")
                st.markdown("**Recommended Number of Specimens**: 3")
                
                with open("ASTM_F1868_Standard.pdf", "rb") as pdf_file:
                    st.download_button(
                        label="Download ASTM F1868 Standard (PDF)",
                        data=pdf_file,
                        file_name="ASTM_F1868_Standard.pdf",
                        mime="application/pdf"
                )
            
            if st.checkbox("Alternative Method - Modified Transient Plane Source (MTPS)"):
                st.markdown("**Metric**: Using MTPS, thermal conductivity is measured. Having thickness of the material, thermal resistance is calculated.")
                st.markdown("**Relevant Standard**: MTPS - **ASTM** **D7984**")
                st.markdown("**Sample Size**: 10cm X 10cm")
                st.markdown("**Recommended Number of Specimens**: 5")
                
                with open("ASTM_D7984_Standard.pdf", "rb") as pdf_file:
                   st.download_button(
                       label="Download ASTM D7984 Standard (PDF)",
                       data=pdf_file,
                       file_name="ASTM_D7984_Standard.pdf",
                       mime="application/pdf"
                   )
                   
        with st.expander("Breathability"):
            if st.checkbox("Evaporative Resistance"):
                st.markdown("**Metric**: Evaporative resistance REF,  a quantity specific to textile materials or composites, determines the latent evaporative heat flux across a given area in response to a steady applied water-vapour pressure gradient.")
                st.markdown("**Relevant Standard**: Sweating Guarded Hot Plate - **ASTM** **F1868 - Part B**")
                st.markdown("**Sample Size**: 30cm X 30cm")
                st.markdown("**Recommended Number of Specimens**: 3")
                with open("ASTM_F1868_Standard.pdf", "rb") as pdf_file:
                    st.download_button(
                        label="Download ASTM F1868 Standard (PDF)",
                        data=pdf_file,
                        file_name="ASTM_F1868_Standard.pdf",
                        mime="application/pdf"
            )
            
            if st.checkbox("Water Vapor Transmission Rate"):
                st.markdown("**Metric**: g/m$^2$/h$^1$, The number of grams of sweat passing through a square meter fabric in 24 hours.")
                st.markdown("**Relevant Standard**: Water Vapor Permeability Tester - **ISO** **15496**")
                st.markdown("**Sample Size**: Three circular specimens of the fabric with diameter of approximately 180 mm")
                st.markdown("**Recommended Number of Specimens**: 3")
                with open("ISO_15496_Standard.pdf", "rb") as pdf_file:
                    st.download_button(
                        label="Download ISO 15496 Standard (PDF)",
                        data=pdf_file,
                        file_name="ISO_15496_Standard.pdf",
                        mime="application/pdf"
            )
            
        with st.expander("Moisture Management"):
            if st.checkbox("Horizontal Wicking"):
                st.markdown("**Metric**: Lengthwise and widthwise wicking distances in a certain time (2 or 5 minutes) for 1 mL of water.")
                st.markdown("**Relevant Standard**: Horizontal Wicking of Textiles - **AATCC** **TM198**")
                st.markdown("**Sample Size**: Flexbility of sample size - Preferrably larger than 18cm X 18cm ")
                st.markdown("**Recommended Number of Specimens**: 3")
            if st.checkbox("Vertical Wicking"):
                st.markdown("**Metric**: Time at a given vertical distance or vertical distance in a given time.")
                st.markdown("**Relevant Standard**: Vertical Wicking of Textiles- **AATCC** **TM197**")
                st.markdown("**Sample Size**: at least three samples of fabric in 18cm X 2.5cm size ")
                st.markdown("**Recommended Number of Specimens**: 3")      
            if st.checkbox("Dry Rate"):
                st.markdown("**Metric**: Drying rate (mL/h) which indicates how quickly a fabrics dries in a certain environment condition.")
                st.markdown("**Relevant Standard**: Test Method for Drying Rate of Fabrics - Heated Plate  - **AATCC** **TM201**")
                st.markdown("**Sample Size**: Three specimens of the fabric with at least 20cm X 20cm size")
                st.markdown("**Recommended Number of Specimens**: 5")
                with open("AATCC TM_201_ Standard.pdf", "rb") as pdf_file:
                    st.download_button(
                        label="AATCC TM_201_ Standard (PDF)",
                        data=pdf_file,
                        file_name="AATCC TM_201_ Standard.pdf",
                        mime="application/pdf"
                        )
            
            if st.checkbox("Water Absorption"):
                st.markdown("**Metric**: Absolute Absorption per unit area (g.$m^-2$) which indicates how much water can a fabric absorb per unit area in a certain time when merged in water.")
                st.markdown("**Relevant Standard**: In-House Protocol")
                st.markdown("**Sample Size**: Three specimens of 3in X 3in")
                st.markdown("**Recommended Number of Specimens**: 3")
                
        
        with st.expander("Thermal Hand"):
            if st.checkbox("Thermal Effusivity"):
                st.markdown("**Metric**: Absolute Absorption per unit area (g.$m^-2$) which indicates how much water can a fabric absorb per unit area in a certain time when merged in water.")
                st.markdown("**Relevant Standard**: Standard Test Method for Measurement of Thermal Effusivity of Fabrics - **ASTM** **D7984**")
                st.markdown("**Sample Size**: Five Specimens of Fabrics with Flexible Size")
                st.markdown("**Recommended Number of Specimens**: 5")
                with open("ASTM_D7984_Standard.pdf", "rb") as pdf_file:
                   st.download_button(
                       label="Download ASTM D7984 Standard (PDF)",
                       data=pdf_file,
                       file_name="ASTM_D7984_Standard.pdf",
                       mime="application/pdf"
                       )
    
        with st.expander("Density"):
            if st.checkbox("Fabric Weight"):
                st.markdown("**Metric**: Weight (gsm)")
                st.markdown("**Relevant Standard**: Standard Test Method for Mass Per Unit Area of Fabric - **ASTM** **D3776**")
                st.markdown("**Sample Size**: Die cut of 100 $cm^2$")
                st.markdown("**Recommended Number of Specimens**: 3")
                with open("ASTM_D3776_Standard.pdf", "rb") as pdf_file:
                   st.download_button(
                       label="Download ASTM D3776 Standard (PDF)",
                       data=pdf_file,
                       file_name="ASTM_D3776_Standard.pdf",
                       mime="application/pdf"
                       )
                
            if st.checkbox("Fabric Thickness"):
                st.markdown("**Metric**: Thickness (mm).")
                st.markdown("**Relevant Standard**: Determination of Thickness of Textiles and Textiles Products - **ISO** **5084**")
                st.markdown("**Sample Size**: Specimens of Fabrics with Flexible Size")
                st.markdown("**Recommended Number of Specimens**: 5")
                with open("ISO_5084_Standard.pdf", "rb") as pdf_file:
                   st.download_button(
                       label="Download ISO 5084 Standard (PDF)",
                       data=pdf_file,
                       file_name="ISO_5084_Standard.pdf",
                       mime="application/pdf"
                       )

def main():
    st.set_page_config(
        page_title="Materials Testing Hub",
        page_icon=":scissors:",
        layout="wide",
    )

    # Define tabs
    tabs = st.tabs(["Radar Charts & Features", "Other Features"])

    with tabs[0]:
        st.title("Materials Testing Hub")
        MaterialsTestingHub()  # Display radar charts and popovers together

    with tabs[1]:
        st.title("Other Features")
        st.markdown("This is where you can add more features or tools for the app.")

if __name__ == "__main__":
    main()
