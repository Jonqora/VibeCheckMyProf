
# Create API Gateway
resource "aws_api_gateway_rest_api" "professor_api" {
  name = "ProfessorDataAPI"
}

resource "aws_api_gateway_resource" "professor" {
  rest_api_id = aws_api_gateway_rest_api.professor_api.id
  parent_id   = aws_api_gateway_rest_api.professor_api.root_resource_id
  path_part   = "professor"
}

resource "aws_api_gateway_method" "get_professor" {
  rest_api_id   = aws_api_gateway_rest_api.professor_api.id
  resource_id   = aws_api_gateway_resource.professor.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id = aws_api_gateway_rest_api.professor_api.id
  resource_id = aws_api_gateway_resource.professor.id
  http_method = aws_api_gateway_method.get_professor.http_method
  type        = "AWS_PROXY"
  uri         = aws_lambda_function.on_demand_professor_data.invoke_arn
}

resource "aws_lambda_permission" "apigw_lambda" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.on_demand_professor_data.arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.professor_api.execution_arn}/*/*"
}

resource "aws_api_gateway_deployment" "api_deployment" {
  depends_on   = [aws_api_gateway_integration.lambda_integration]
  rest_api_id  = aws_api_gateway_rest_api.professor_api.id
  stage_name   = "prod"
}