from flask import Response, redirect, url_for

class HttpStatus:
    
    def Ok(self, data=None, contentType='application/json'):
        return Response(data, status=200, mimetype=contentType)
    
    def BadRequest(self, error='Bad Request'):
        return Response(error, status=400)
        
    def NotFound(self, error='Not Found'):
        return Response(error, status=404)
        
    def InternalServerError(self, error='Internal Server Error'):
        return Response(error, status=500)
        
    def Unauthorized(self, error='Unauthorized'):
        return Response(error, status=401)
