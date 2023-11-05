from flask import Flask, request, jsonify
import joblib
app = Flask(__name__)

fModel2 = './mon_modele2.pkl'
fModel1 = './mon_modele.pkl'


isModel1 = False

model = joblib.load(fModel1) if isModel1 else joblib.load(fModel2) 
vecteur = './mon_vecteur.pkl' if isModel1 else './mon_vecteur2.pkl'

def decodeurBinaire(valeurBinaire) : 
    arrType = [
    "toxic",
    "severe_toxic",
    "obscene",
    "threat",
    "insult",
    "identity,_hate"
]

    typologie = 'faites attention au propos que vous tenez, car ils sont'
    if valeurBinaire != '0000':
        for i in range (len(valeurBinaire)) : 
            print(int(valeurBinaire[i]) == 1)
            if int(valeurBinaire[i]) == 1 :
                typologie += ' ' +  arrType[i]
    else :
        typologie = 'votre texte est conforme à ce que nous demandons'
    return typologie

with open(vecteur, 'rb') as f:
    vecteurizer = joblib.load(f) 


joblib.dump(vecteurizer, vecteur)

# Route POST
@app.route('/api/data', methods=['POST'])
def post_data():
    data = request.get_json()
    nouvelle_phrase = data['message']
    vecteur_entree = vecteurizer.transform([nouvelle_phrase])
    prediction = model.predict(vecteur_entree)

    if isModel1 : 
        valeurBinaire = str('{:06b}'.format(prediction[0]))[2:]
        typologie = decodeurBinaire(valeurBinaire)
    else : 
        typologie = " faites attention au propos que vous tenez, car ils sont inadapté" if prediction[0] == 1 else "vos propos sont approprié"
    
    if data:
        return jsonify({'message':typologie})
    else:
        return jsonify({'message': 'Erreur : Aucune donnée POST n\'a été fournie.'}), 400


if __name__ == '__main__':
    app.run(debug=True)