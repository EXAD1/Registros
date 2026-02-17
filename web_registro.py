from supabase import create_client, Client
import qrcode
import streamlit as st
import numpy as np

# 1. Datos de conexión
URL_PROYECTO = "https://kofceetypfxcwxhvqsla.supabase.co"
LLAVE_API = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtvZmNlZXR5cGZ4Y3d4aHZxc2xhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA5NDk1MDIsImV4cCI6MjA4NjUyNTUwMn0.hLcMPTCVHNzc4cJZdxzF60fH1vyRzCcQrtweNaCFM-4"

# 2. Conexión limpia (Sin parches, porque ya estarás en 3.12)
supabase: Client = create_client(URL_PROYECTO, LLAVE_API)

def generar_ID (nom_inv, apellido, numero):
    token = nom_inv[0:3:2] + apellido[0:3:2] + str(numero)
    return token
st.title("🎟️ Registro de Invitados")

 
nom_inv = st.text_input("Ingrese el nombre del invitado: ")
apellido = st.text_input("Ingrese el apellido del invitado: ")
nom_vend = st.text_input("Ingrese el nombre del vendedor: ")
numero = st.text_input("Ingresa un numero del 1 al 9: ", key="numero_input")

if st.button("Registrar Invitado"):
    if not numero.isdigit():
        st.error("Debes ingresar un número del 1 al 9.")
    else:
        numero = int(numero)

    if numero < 1 or numero > 9:
        st.error("El número debe estar entre 1 y 9.")
    tok = generar_ID(nom_inv, apellido, numero)

    # 3. Invitado
    datos_invitado = {
        "nombre": nom_inv + " " + apellido,
        "vendedor": nom_vend,
        "token_qr": tok,
        "ingresado": False
    }



    imagen = qrcode.make(tok)
    file_name = f"pase_{nom_inv}.png"
    
    imagen.save(file_name)
    
    with open(file_name, "rb") as file:
        st.download_button(
            label="📥 Descargar pase QR",
            data=file,
            file_name=file_name,
            mime="image/png"
        )

    # 4. El envío
    st.text("🚀 Conectando con la nube estable...")
    try:
        respuesta = supabase.table("invitados").insert(datos_invitado).execute()
        st.success("✅ ¡ÉXITO TOTAL! Revisa tu tabla en la web de Supabase.")
    except Exception as e:
        if "duplicate" in str(e):
            st.error(f"Error: El token '{tok}' ya existe en la base de datos. Por favor, genera un nuevo token.")
        else:
            st.error(f"Ocurrió un error inesperado: {e}")

    if st.button("Registrar otro Invitado"):
        st.rerun()
        
        #print("Desea registrar otro invitado? (s/n)")
        #continuar = st.text_input("¿Desea registrar otro invitado? (s/n): ").lower()
        #if continuar == 'n':
        #    st.text("¡Hasta luego! 👋")
        #    break
        #elif continuar != 's':
        #    st.text("Entrada no válida. Saliendo del programa.")
        #    break '''

        

