# Importación librerías
from flask import Flask
from flask_restx import Api, Resource, fields
from flask_cors import CORS
import joblib
import pandas as pd

# Definición aplicación Flask
app = Flask(__name__)

CORS(app)
# Definición API Flask
api = Api(
    app, 
    version='1.0', 
    title='Car Price Prediction API',
    description='Car Price Prediction API')

# Definición argumentos o parámetros de la API
parser = api.parser()
parser.add_argument('year', type=int, required=True, help='Año o year', location='args')
parser.add_argument('mileage', type=int, required=True, help='Kilometraje o mileage', location='args')
parser.add_argument('State', type=str, required=True, help='Estado o state: FL, OH,TX, CO, ME, WA, CT, CA, LA, NY,  PA,  SC,  ND,  NC,  GA,  AZ,  TN, KY, NJ,  UT,  IA,  AL,  NE,  IL,  OK,  MD, NV, WV,  MI,  VA,  WI,  MA,  OR,  IN,  NM, MO, HI,  KS,  AR,  MN,  MS,  MT,  AK,  VT, SD, NH,  DE,  ID,  RI,  WY,  DC', location='args')
parser.add_argument('Make', type=str, required=True, help='Fabricante: Jeep, Chevrolet, BMW, Cadillac, Mercedes-Benz, Toyota, Buick, Dodge, Volkswagen, GMC, Ford, Hyundai, Mitsubishi, Honda, Nissan, Mazda, Volvo, Kia, Subaru, Chrysler, INFINITI, Land, Porsche, Lexus, MINI, Lincoln, Audi, Ram, Mercury, Tesla, FIAT, Acura, Scion, Pontiac, Jaguar, Bentley, Suzuki, Freightliner', location='args')
parser.add_argument('Model', type=str, required=True, help='Modelo: Wrangler, Tahoe4WD, X5AWD, SRXLuxury, 3, C-ClassC300, CamryL, TacomaPreRunner, LaCrosse4dr, ChargerSXT, CamryLE, Jetta, AcadiaFWD, EscapeSE, SonataLimited, Santa, Outlander, CruzeSedan, Civic, CorollaL, 350Z2dr, EdgeSEL, F-1502WD, FocusSE, PatriotSport, Accord, MustangGT, FusionHybrid, ColoradoCrew, Wrangler4WD, CR-VEX-L, CTS, CherokeeLimited, Yukon, Elantra, New, CorollaLE, Canyon4WD, Golf, Sonata4dr, Elantra4dr, PatriotLatitude, Mazda35dr, Tacoma2WD, Corolla4dr, Silverado, TerrainFWD, EscapeFWD, Grand, RAV4FWD, Liberty4WD, FocusTitanium, DurangoAWD, S60T5, CivicLX, MuranoAWD, ForteEX, TraverseAWD, CamaroConvertible, Sportage2WD, Pathfinder4WD, Highlander4dr, WRXSTI, Ram, F-150XLT, SiennaXLE, LaCrosseFWD, RogueFWD, CamaroCoupe, JourneySXT, AccordEX-L, Escape4WD, OptimaEX, FusionSE, 5, F-150SuperCrew, 200Limited, Malibu, CompassSport, G37, CanyonCrew, Malibu1LT, MustangPremium, MustangBase, Sierra, FlexLimited, Tahoe2WD, Transit, Outback2.5i, TucsonLimited, Rover, CayenneAWD, MalibuLT, TucsonFWD, F-150FX2, Camaro2dr, Colorado4WD, SonataSE, ESES, EnclavePremium, CR-VEX, F-150STX, Impreza, EquinoxFWD, Cooper, Super, Passat4dr, 911, CivicEX, CamrySE, Highlander4WD, Corvette2dr, 200S, PilotLX, SorentoEX, RioLX, ExplorerXLT, CorvetteCoupe, EnclaveLeather, Avalanche4WD, TacomaBase, Versa5dr, MKXFWD, SL-ClassSL500, VeracruzFWD, CorollaS, PriusTwo, CR-V2WD, Lucerne4dr, 4Runner4dr, PilotTouring, CR-VLX, CompassLatitude, Altima4dr, OptimaLX, Focus5dr, Charger4dr, AcadiaAWD, JourneyFWD, 7, RX, MalibuLS, LSLS, SportageLX, Yukon4WD, SorentoLX, TiguanSEL, Camry4dr, F-1504WD, PriusBase, AccordLX, Q7quattro, ExplorerLimited, 4RunnerSR5, OdysseyEX-L, C-ClassC, CX-9FWD, JourneyAWD, Sorento2WD, F-250Lariat, Prius, TahoeLT, 25004WD, Escalade4dr, GTI4dr, 4RunnerRWD, FX35AWD, XC90T6, Taurus4dr, AvalonXLE, 300300S, G35, F-150Platinum, TerrainAWD, GXGX, MKXAWD, Town, CamryXLE, VeracruzAWD, FusionS, Challenger2dr, Tundra, Navigator4WD, Legacy3.6R, GS, E-ClassE350, Suburban2WD, A44dr, RegalTurbo, Outback3.6R, 4Runner4WD, Legacy2.5i, 1, Yukon2WD, Explorer, PilotEX-L, 200LX, M-ClassML350, RAV4XLE, WranglerSport, Model, FJ, Titan, Titan4WD, FlexSEL, OdysseyTouring, SorentoSX, RAV4Base, OdysseyEX, Explorer4WD, Mustang2dr, EdgeLimited, FusionSEL, Yukon4dr, Touareg4dr, Matrix5dr, CTCT, CherokeeSport, 6, Maxima4dr, Frontier4WD, PriusThree, F-350XL, 500Pop, RDXAWD, Tacoma4WD, Optima4dr, Q5quattro, X3xDrive28i, RDXFWD, X5xDrive35i, Malibu4dr, ExpeditionXLT, Ranger2WD, Patriot4WD, Quest4dr, TaurusSE, PathfinderS, Murano2WD, LS, SiennaLimited, ES, SiennaLE, F-150Lariat, Titan2WD, Durango2WD, Tahoe4dr, Focus4dr, YarisBase, TaurusLimited, RAV44WD, C-Class4dr, Soul+, TundraBase, Expedition, ImpalaLT, SedonaLX, Sequoia4WD, ElantraLimited, 15002WD, Suburban4WD, FiestaSE, 15004WD, TundraSR5, Camry, RAV4Limited, RangerSuperCab, MDXAWD, RAV4LE, ChallengerR/T, FlexSE, ForteLX, TraverseFWD, LibertySport, ISIS, Impala4dr, Tundra4WD, F-250XLT, RXRX, Armada2WD, Frontier, WranglerRubicon, EquinoxAWD, PilotEX, TiguanS, EscaladeAWD, DTS4dr, Pilot2WD, Express, PacificaLimited, CanyonExtended, MX5, EscapeS, IS, C-ClassC350, Compass4WD, SportageEX, Legacy, E-ClassE, Dakota4WD, 300300C, Forte, SportageAWD, TaurusSEL, Xterra4WD, GSGS, Explorer4dr, F-150XL, SportageSX, xB5dr, TundraLimited, CruzeLT, Wrangler2dr, HighlanderFWD, Sprinter, Highlander, Prius5dr, CX-9Grand, CTS4dr, Econoline, AccordEX, RAV4Sport, 35004WD, ChargerSE, OdysseyLX, TucsonAWD, CX-7FWD, AccordLX-S, Navigator4dr, EscapeXLT, TiguanSE, Cayman2dr, TaurusSHO, F-150FX4, Ranger4WD, OptimaSX, SequoiaSR5, G64dr, HighlanderLimited, ExplorerFWD, F-350King, PriusFive, Yaris4dr, PatriotLimited, Lancer4dr, HighlanderSE, CompassLimited, S2000Manual, F-250King, Forester2.5X, Fusion4dr, Frontier2WD, FocusST, Pathfinder2WD, Sentra4dr, XF4dr, F-250XL, PacificaTouring, MustangDeluxe, Caliber4dr, GTI2dr, Mazda34dr, FocusS, Sienna5dr, CR-V4WD, CX-9Touring, Mazda64dr, Forester4dr, 1500Tradesman, MDX4WD, Escalade, TL4dr, Canyon2WD, A64dr, A8, Armada4WD, Impreza2.0i, GX, QX564WD, CC4dr, MKZ4dr, Yaris, FitSport, Regal4dr, Tundra2WD, X3AWD, SonicSedan, Cobalt4dr, RidgelineRTL, CivicSi, AvalancheLimited, XC90FWD, Outlander2WD, RAV44dr, ColoradoExtended, ExpeditionLimited, 3004dr, 200Touring, SC, X1xDrive28i, SonicHatch, GLI4dr, PilotSE, Savana, RegalPremium, CR-VSE, RegalGS, XC90AWD, EdgeSport, PriusFour, SiennaSE, 1500Laramie, 300Base, Pilot4WD, A34dr, HighlanderBase, Expedition4WD, STS4dr, SoulBase, Xterra2WD, CT, tC2dr, Tiguan2WD, CR-ZEX, MustangShelby, C702dr, WranglerX, WranglerSahara, DurangoSXT, Sequoia4dr, Outlander4WD, Expedition2WD, Navigator, 9112dr, Vibe4dr, F-150King, 300Limited, XC60T6, CivicEX-L, Avalanche2WD, F-350XLT, ExplorerBase, MuranoS, LXLX, EdgeSE, ImpalaLS, Land, E-ClassE320, Milan4dr, Boxster2dr, RAV4, Eos2dr, SedonaEX, xD5dr, Colorado2WD, Monte, Escape4dr, LX, FiestaS, F-350Lariat, Galant4dr, TT2dr, Xterra4dr, SequoiaLimited, 4RunnerLimited, Genesis, Suburban4dr, EnclaveConvenience, LaCrosseAWD, Versa4dr, Cobalt2dr, XC60FWD, F-150Limited, Dakota2WD, S44dr, 4Runner2WD, Sedona4dr, RidgelineSport, TSXAutomatic, ImprezaSport, SLK-ClassSLK350, Accent4dr, CorvetteConvertible, Avalon4dr, Passat, 25002WD, ExplorerEddie, LibertyLimited, CTS-V, 4RunnerTrail, Eclipse3dr, Azera4dr, TahoeLS, Continental, XJ4dr, ForteSX, SequoiaPlatinum, FocusSEL, Durango4dr, CamryBase, XC704dr, S804dr, Element4WD, YarisLE, WRXBase, TLAutomatic, AvalonTouring, XK2dr, PT, PathfinderSE, 300Touring, Navigator2WD, XC60AWD, EscapeLimited, WRXLimited, AccordSE, QX562WD, Escalade2WD, EscapeLImited, PriusOne, Element2WD, Excursion137", WRXPremium, RX-84dr.', location='args')

# modelo entrenado
modelo = joblib.load('price_prediction_clf.pkl')
encoder = joblib.load('encoder.pkl')

resource_fields = api.model('Resource', {'result': fields.Float})

class CarPriceApi(Resource):
    @api.expect(parser)
    def get(self):
        args = parser.parse_args()
        year = args['year']
        mileage = args['mileage']
        state = args['State']
        make = args['Make']
        model = args['Model']

        X = {'year': [year], 'mileage': [mileage], 'State': [state], 'Make': [make], 'Model': [model]}
        df = pd.DataFrame(X)
  
        # Codificar las variables categóricas utilizando TargetEncoder
        X_encoded = encoder.transform(df)
        #print(X_encoded)
        
        year, mileage, State, Make, Model = X_encoded.values.tolist()[0]
        #print('year', year,'mileage', mileage, 'state', State,'make', Make, 'model',Model)
    
        features = [[year, mileage, State, Make, Model]]
        prediccion = str(modelo.predict(features))
        
        return {'result': prediccion}, 200

api.add_resource(CarPriceApi, '/car_price') 

# Ejecución de la aplicación que disponibiliza el modelo de manera local en el puerto 5000
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)
