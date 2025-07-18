import sys
import importlib.util
import os

def load_module_from_file(file_path):
    """
    파일에서 모듈을 동적으로 로드하는 함수
    """
    try:
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        print(f"❌ 파일 로드 실패: {e}")
        return None

def test_hello_function(module):
    """
    모듈의 Hello 함수를 테스트하는 함수
    """
    try:
        # Hello 함수가 존재하는지 확인
        if not hasattr(module, 'Hello'):
            print("❌ 테스트 실패: Hello 함수를 찾을 수 없습니다.")
            return False
        
        # Hello 함수 호출
        hello_func = getattr(module, 'Hello')
        result = hello_func()
        
        # 출력값 검사
        expected_output = "hello"
        
        print(f"함수 출력값: {result}")
        print(f"예상 출력값: {expected_output}")
        
        # 반환값 타입 검사
        if not isinstance(result, str):
            print("❌ 타입 검사 실패: 반환값이 문자열이 아닙니다.")
            return False
        else:
            print("✅ 타입 검사 통과: 반환값이 문자열입니다.")
        
        # 출력값 내용 검사
        if result == expected_output:
            print("✅ 테스트 통과: 출력값이 올바릅니다!")
            return True
        else:
            print("❌ 테스트 실패: 출력값이 예상과 다릅니다.")
            return False
            
    except Exception as e:
        print(f"❌ 함수 실행 중 오류 발생: {e}")
        return False

def main():
    """
    메인 함수: test1.py 파일에서 Hello 함수를 테스트
    """
    # test1.py 파일을 자동으로 찾음
    file_path = "test1.py"
    
    # 파일 존재 확인
    if not os.path.exists(file_path):
        print(f"❌ test1.py 파일을 찾을 수 없습니다.")
        sys.exit(1)
    
    print("🔍 Python 문제 출력 검사 프로그램")
    print("=" * 50)
    print("📋 문제: Hello 함수를 작성하세요")
    print("   - 함수명: Hello")
    print("   - 반환값: 문자열 'hello'")
    print("   - 반환 타입: str")
    print("=" * 50)
    print(f"📁 테스트 파일: {file_path}")
    print("=" * 50)
    
    # 모듈 로드
    module = load_module_from_file(file_path)
    if module is None:
        sys.exit(1)
    
    # Hello 함수 테스트
    test_result = test_hello_function(module)
    
    print("=" * 50)
    if test_result:
        print("🎉 전체 테스트 통과!")
    else:
        print("💥 테스트 실패!")
    
    return test_result

if __name__ == "__main__":
    main()
