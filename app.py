import numpy as np
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import pickle

app = Flask(__name__)
CORS(app)
model = pickle.load(open("model.pkl", "rb"))

try:
    with open("names.pkl", "rb") as f:
        names = pickle.load(f)
except FileNotFoundError:
    print("Atenção: Arquivo 'names.pkl' não encontrado! Usando valores padrão...")
    names = {
        0: "Peso Insuficiente",
        1: "Peso Normal",
        2: "Sobrepeso Nível I",
        3: "Sobrepeso Nível II",
        4: "Obesidade Tipo I",
        5: "Obesidade Tipo II",
        6: "Obesidade Tipo III"
    }

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Pegando os valores do formulário
        features = request.form.to_dict()

        # 🔹 Convertendo altura para metros (se o usuário inserir em cm)
        features["height"] = float(features["height"]) / 100  
        
        # 🔹 Convertendo os demais valores para float
        numerical_fields = ["age", "weight", "ncp", "ch2o", "fcvc", "faf", "tue"]
        for field in numerical_fields:
            features[field] = float(features[field])

        # 🔹 Convertendo os valores categóricos para números
        categorical_mappings = {
            "gender": {"0": 0, "1": 1},
            "family_history": {"0": 0, "1": 1},
            "caec": {"0": 0, "1": 1, "2": 2},
            "calc": {"0": 0, "1": 1, "2": 2},
            "mtrans": {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4},
        }

        for key, mapping in categorical_mappings.items():
            if key in features:
                features[key] = mapping[features[key]]  # Converte string para número

        # 🔹 Preparando os dados para o modelo
        final_features = np.array([list(features.values())]).reshape(1, -1)

        # 🔹 Fazendo a predição
        pred = model.predict(final_features)
        
        output = names.get(pred[0], "Desconhecido")

        return render_template("index.html", prediction_text=f"Nível de Obesidade: {output}")

    except Exception as e:
        return render_template("index.html", prediction_text=f"Erro na previsão: {str(e)}")

@app.route("/api", methods=["POST"])
def results():
    try:
        data = request.get_json(force=True)
        pred = model.predict([np.array(list(data.values()))])
        output = pred[0]
        return jsonify({"obesity_level": output})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)