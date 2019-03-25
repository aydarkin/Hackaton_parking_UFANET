//
//  ViewController.swift
//  Ufanet Parking
//
//  Created by Раиль Абдуллин on 24.03.2019.
//  Copyright © 2019 СРП Хобби. All rights reserved.
//

import UIKit
import SpriteKit

class ViewController: UIViewController {

    @IBOutlet weak var freePlacesAmountL: UILabel!
    @IBOutlet weak var occupiedPlacesAmountL: UILabel!
    @IBOutlet weak var image: UIImageView!
    
    //id ближайшего ко въезду парковочного места
    let firstParkingPlaceID = 0;
    
    let beginPoint = CGPoint(x: 151, y: 22) //320 0
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }
    
    override func viewWillAppear(_ animated: Bool) {
        var responseString = "null"
        let needEthernet = true
        let url = URL(string: "http://84.201.147.156:8080")!
        var request2 = URLRequest(url: url)
        request2.setValue("application/x-www-form-urlencoded", forHTTPHeaderField: "Content-Type")
        request2.httpMethod = "POST"
        var postString2 = ""
        print("postString=\(postString2)")
        request2.httpBody = postString2.data(using: .utf8)
        
        let task2 = URLSession.shared.dataTask(with: request2) { data, response, error in
            guard let data = data, error == nil else { // check for fundamental networking error
                print("error=\(error ?? "null" as! Error)")
                if needEthernet==true {
                    DispatchQueue.main.async {
                        let alert = UIAlertController(title: "Для работы приложения необходимо интернет соединение", message: "", preferredStyle: UIAlertController.Style.alert)
                        alert.addAction(UIAlertAction(title: "OK", style: UIAlertAction.Style.cancel, handler: nil))
                        self.present(alert, animated: true, completion: nil)
                    }
                }
                return
            }
            
            if let httpStatus = response as? HTTPURLResponse, httpStatus.statusCode != 200 { // check for http errors
                DispatchQueue.main.async {
                    let alert = UIAlertController(title: "Oh, something went wrong", message: "We received error information and will fix it soon.", preferredStyle: UIAlertController.Style.alert)
                    let alertAction = UIAlertAction(title: "OK", style: UIAlertAction.Style.default){
                        (UIAlertAction) -> Void in
                    }
                    alert.addAction(alertAction)
                    self.present(alert, animated: true, completion: nil)
                    
                }
            }
            responseString = String(data: data, encoding: .utf8) ?? "null"
            print(responseString)
            if responseString == "" || responseString == nil {
                DispatchQueue.main.async {
                    let alert = UIAlertController(title: "Ответ не получен:(", message: " в", preferredStyle: UIAlertController.Style.alert)
                    let alertAction = UIAlertAction(title: "OK", style: UIAlertAction.Style.default){
                        (UIAlertAction) -> Void in
                    }
                    alert.addAction(alertAction)
                    self.present(alert, animated: true, completion: nil)
                    
                }
            } else {
                DispatchQueue.main.async {
                    do {
                        let decoder = JSONDecoder()
                        let decodedJSON = try? decoder.decode(jsonKeys.mainJSON.self, from: data)
                        dump(decodedJSON)
                        if decodedJSON != nil {
                            self.freePlacesAmountL.text = decodedJSON!.free!
                            self.occupiedPlacesAmountL.text = "Занятых мест: " + decodedJSON!.busy!
                            if decodedJSON?.image != "" && decodedJSON != nil {
                                let dataDecoded : Data = Data(base64Encoded: (decodedJSON?.image)!, options: .ignoreUnknownCharacters)!
                                if  dataDecoded != nil {
                                    let decodedimage = UIImage(data: dataDecoded)
                                    if decodedimage != nil {
                                        self.image.setCustomImage("http://84.201.147.156:8080/static/frame.jpg")
                                    }
                                }
                            }
                            
                        }
                    }
                }
            }
        }
        task2.resume()
        
        //drawRoute(id: 1)
    }
    
    
    func drawRoute(id: Int) {
        
        
        let scale = UIScreen.main.scale
        UIGraphicsBeginImageContextWithOptions((image.image?.size)!, false, scale)
        let context = UIGraphicsGetCurrentContext()
        image.image?.draw(in: CGRect(origin: CGPoint.zero, size: (image.image?.size)!))
        
        switch id {
        case 1:
            context?.move(to: beginPoint)
            context?.addLine(to: CGPoint(x: 201, y: 22))
            context?.addLine(to: CGPoint(x: 250, y: 40))
            context?.addLine(to: CGPoint(x: 250, y: 55))
            break
            
        case 2:
            context?.move(to: beginPoint)
            context?.addLine(to: CGPoint(x: 300, y: 15))
            context?.addLine(to: CGPoint(x: 330, y: 35))
            context?.addLine(to: CGPoint(x: 306, y: 135))
            context?.addLine(to: CGPoint(x: 370, y: 203))
            break
            
        case 3:
            context?.move(to: beginPoint)
            context?.addLine(to: CGPoint(x: 300, y: 15))
            context?.addLine(to: CGPoint(x: 330, y: 35))
            context?.addLine(to: CGPoint(x: 295, y: 187))
            context?.addLine(to: CGPoint(x: 200, y: 273))
            break
            
        case 4:
            context?.move(to: beginPoint)
            context?.addLine(to: CGPoint(x: 300, y: 15))
            context?.addLine(to: CGPoint(x: 330, y: 35))
            context?.addLine(to: CGPoint(x: 278, y: 295))
            context?.addLine(to: CGPoint(x: 330, y: 440))
            break
            
        case 5:
            context?.move(to: beginPoint)
            context?.addLine(to: CGPoint(x: 300, y: 15))
            context?.addLine(to: CGPoint(x: 330, y: 35))
            
            context?.addLine(to: CGPoint(x: 242, y: 455))
            context?.addLine(to: CGPoint(x: 152, y: 574))
            break
            
        case 6:
            context?.move(to: beginPoint)
            context?.addLine(to: CGPoint(x: 300, y: 15))
            context?.addLine(to: CGPoint(x: 330, y: 35))
            
            context?.addLine(to: CGPoint(x: 200, y: 620))
            //поворот
            context?.addLine(to: CGPoint(x: 311, y: 720))
            context?.addLine(to: CGPoint(x: 509, y: 764))
            //парковка
            context?.addLine(to: CGPoint(x: 332, y: 842))
            break
            
        case 7:
            context?.move(to: beginPoint)
            context?.addLine(to: CGPoint(x: 300, y: 15))
            context?.addLine(to: CGPoint(x: 330, y: 35))
            
            context?.addLine(to: CGPoint(x: 200, y: 620))
            //поворот
            context?.addLine(to: CGPoint(x: 311, y: 720))
            context?.addLine(to: CGPoint(x: 509, y: 744))
            //парковка
            context?.addLine(to: CGPoint(x: 426, y: 675))
            context?.addLine(to: CGPoint(x: 410, y: 560))
            break
            
        case 8:
            context?.move(to: beginPoint)
            context?.addLine(to: CGPoint(x: 300, y: 15))
            context?.addLine(to: CGPoint(x: 330, y: 35))
            
            context?.addLine(to: CGPoint(x: 200, y: 620))
            //поворот
            context?.addLine(to: CGPoint(x: 311, y: 720))
            context?.addLine(to: CGPoint(x: 619, y: 744))
            //парковка
            context?.addLine(to: CGPoint(x: 515, y: 675))
            context?.addLine(to: CGPoint(x: 510, y: 560))
            break
            
        case 9:
            context?.move(to: beginPoint)
            context?.addLine(to: CGPoint(x: 300, y: 15))
            context?.addLine(to: CGPoint(x: 330, y: 35))
            
            context?.addLine(to: CGPoint(x: 200, y: 620))
            //поворот
            context?.addLine(to: CGPoint(x: 311, y: 720))
            
            
            context?.addLine(to: CGPoint(x: 739, y: 744))
            //парковка
            context?.addLine(to: CGPoint(x: 635, y: 675))
            context?.addLine(to: CGPoint(x: 630, y: 560))
            break
        
        case 10:
            context?.move(to: beginPoint)
            context?.addLine(to: CGPoint(x: 300, y: 15))
            context?.addLine(to: CGPoint(x: 330, y: 35))
            
            context?.addLine(to: CGPoint(x: 200, y: 620))
            //поворот
            context?.addLine(to: CGPoint(x: 311, y: 720))
            
            
            context?.addLine(to: CGPoint(x: 739, y: 744))
            //парковка
            context?.addLine(to: CGPoint(x: 635, y: 675))
            context?.addLine(to: CGPoint(x: 630, y: 560))
            break
        default:
            print("def")
            break
        }
        
        
        
        context?.setBlendMode(CGBlendMode.normal)
        context?.setLineCap(CGLineCap.round)
        context?.setLineWidth(10)
        context?.setStrokeColor(UIColor(red: 245, green: 0, blue: 245, alpha: 1).cgColor)
        context?.strokePath()
        
        image.image = UIGraphicsGetImageFromCurrentImageContext()
        
        //image.image = UIImage(data: UIGraphicsGetImageFromCurrentImageContext()!.pngData()!)
        UIGraphicsEndImageContext()
        
    }
    
    func twoLineRotation(fromPoint: CGPoint, toPoint: CGPoint){
        
        let y = fromPoint.y - (toPoint.y - fromPoint.y) * 0.15
        let x = toPoint.x - (toPoint.x - fromPoint.x) * 0.15
        let middlePont = CGPoint(x: x, y: y)
        
    }
    
    /*
    func resizeImage(image: UIImage, newWidth: CGFloat) -> UIImage {
        
        let scale = newWidth / image.size.width
        let newHeight = image.size.height * scale
        UIGraphicsBeginImageContext(CGSizeMake(newWidth, newHeight))
        image.draw(in: CGRectMake(0, 0, newWidth, newHeight))
        let newImage = UIGraphicsGetImageFromCurrentImageContext()
        UIGraphicsEndImageContext()
        
        return newImage
    }*/

}

