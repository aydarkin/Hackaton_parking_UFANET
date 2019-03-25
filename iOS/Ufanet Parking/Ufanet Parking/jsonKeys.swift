//
//  jsonKeys.swift
//  Ufanet Parking
//
//  Created by Раиль Абдуллин on 24.03.2019.
//  Copyright © 2019 СРП Хобби. All rights reserved.
//

import UIKit

public class jsonKeys: NSObject {
    public struct mainJSON : Codable{
        let free : String?
        let busy : String?
        let image: String?
    }
}
